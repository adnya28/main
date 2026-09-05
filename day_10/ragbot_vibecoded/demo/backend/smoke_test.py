import os

from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY is missing from backend/.env")


llm = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    google_api_key=api_key,
    temperature=0,
)
response = llm.invoke("Reply with exactly: smoke test passed")
print("Text model response:", response.content)

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    google_api_key=api_key,
    task_type="RETRIEVAL_DOCUMENT",
)
vector = embeddings.embed_query("This is a short embedding smoke test.")
print("Embedding vector length:", len(vector))
