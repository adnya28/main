# Objective: To create a chatbot that can answer questions based on the content of a PDF document
# using a vector store and a language model.


# step 1: import necessary packages
import os
from pathlib import Path
import requests
from dotenv import load_dotenv
from pydantic import SecretStr

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from system_prompt import SYSTEM_PROMPT

load_dotenv()

# step 2: load the environment variables from .env file
OPENROUTER_API_KEY=os.environ["OPENROUTER_API_KEY"]
BASE_URL=os.environ["BASE_URL"]
MODEL=os.environ["MODEL"]
EMBEDDING_MODEL=os.environ["EMBEDDING_MODEL"]

# step 3: download a pdf document
DOCUMENT_URL = "https://arxiv.org/pdf/2510.26692"
DOCUMENT_PATH = Path(__file__).parent / "kimi.pdf"
CHROMA_PATH = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = f"kimi_{MODEL.replace('/', '_')}_{EMBEDDING_MODEL.replace('/', '_')}"

API_KEY = SecretStr(OPENROUTER_API_KEY)

def download_pdf(url, file_path):
    if file_path.exists():
        print(f"Using cached PDF: {file_path.name}")
        return

    print(f"Downloading {url}...")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    file_path.write_bytes(response.content)
    print(f"Saved {file_path.name} ({len(response.content) / 1_000_000:.1f} MB)")

download_pdf(DOCUMENT_URL, DOCUMENT_PATH)

# step 4: llm initialization
llm = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0,
    default_headers={"X-Title": "Document RAG on Kimi Paper"}
)

embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
    check_embedding_ctx_length=False
)

# step 5: build the vector store from the document
def build_vector_store():
    store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH)
    )
    if store.get(limit=1)["ids"]:
        print(f"Loaded saved vector store from {CHROMA_PATH.name}/")
        return store

    print(f"Indexing: {DOCUMENT_PATH.name}...")
    docs = PyPDFLoader(str(DOCUMENT_PATH)).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    store.add_documents(chunks)
    print(f"Indexed {len(chunks)} chunks with {EMBEDDING_MODEL} into {CHROMA_PATH.name}/")
    return store

vector_store = build_vector_store()
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Context:\n{context}\n\nQuestion: {question}")
    ]
)

def format_doc(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

rag_chain = prompt | llm | StrOutputParser()

# step 6: define a function to get streaming response from the chatbot
def get_streaming_response(user_input):
    docs = retriever.invoke(user_input)
    pages = sorted({doc.metadata.get("page", 0) + 1 for doc in docs})
    yield ("thinking", f"Found {len(docs)} relevant chunks (pages: {pages}.\n)")
    yield ("thinking", f"Asking {MODEL} via OpenRouter...\n")

    for text in rag_chain.stream({"context": format_doc(docs), "question": user_input}):
        if text:
            yield ("response", text)

# step 7: define a function to handle the chat interface
if __name__ == "__main__":
    print(f"\nChat with Caramel AI {DOCUMENT_PATH.name} using {MODEL}. Type 'quit' to exit\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"quit", "exit"}:
            break
        for kind, text in get_streaming_response(user_input):
            print(text, end="",flush=True)
        print("\n")