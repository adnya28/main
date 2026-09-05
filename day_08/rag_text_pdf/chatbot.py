from dotenv import load_dotenv
import os
import urllib.request
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage,AIMessage
from system_prompt_pdf import SYSTEM_PROMPT

import fitz

load_dotenv()


MODEL = os.environ["MODEL"]

llm = init_chat_model(model=MODEL, model_provider="openrouter", temperature=0)

DOCUMENT_PATH=os.path.join(os.path.dirname(__file__),"attention.pdf")
DOCUMENT_URL="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf"

def download_document(url,file_path):
    if os.path.exists(file_path):
        return
    with urllib.request.urlopen(url,timeout=10) as response:
        content=response.read() #.decode("utf-8")
    with open(file_path,"w", encoding="utf-8") as file:
        file.write(content)


download_document(DOCUMENT_URL,DOCUMENT_PATH)

def load_pdf_text_content(file_path):
    if not os.path.exists(file_path):
        return f"Warning: {file_path} does not exist. Procceeding without the document."
    #with open(file_path,"r", encoding="utf-8") as file:
        #return file.read()
    document = fitz.open(file_path)
    pages_text = []
    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        if text.strip():  # Only add non-empty pages
            pages_text.append(f"Page {page_number}:\n{text.strip()}")

        document.close()
        return "\n\n".join(pages_text)
    


document_content=load_pdf_text_content(DOCUMENT_PATH)
knowledge_base=f"{SYSTEM_PROMPT}\n \n Provide an answer to the user's question only from this document {document_content}"

messages: list[BaseMessage]=[SystemMessage(content=knowledge_base)]

def get_streaming_response(user_input):
    global messages
    messages.append(HumanMessage(content=user_input))

    full_response=""
    for chunk in llm.stream(messages):
        content=chunk.content
        if isinstance(content, str) and content:
            full_response+=content
            yield ("response", content)

    messages.append(AIMessage(content=full_response))


