import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

EMBEDDING_MODEL= os.environ["EMBEDDING_MODEL"]
BASE_URL= os.environ["BASE_URL"]

API_KEY=os.environ["OPENROUTER_API_KEY"]


embeddings =OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=BASE_URL,
    api_key= API_KEY,
    check_embedding_ctx_length=False 

)

vector = embeddings.embed_query("home loan eligibility")
print("text         : 'home loan eligibility'")
print("vector dim   :",len(vector))
print("first 5 dims :" ,[round(x,4) for x in vector[:5]])

