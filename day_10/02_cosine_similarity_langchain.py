import os
import math
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

EMBEDDING_MODEL= os.environ["EMBEDDING_MODEL"]
BASE_URL= os.environ["BASE_URL"]

API_KEY = SecretStr(os.environ["OPENROUTER_API_KEY"])

embeddings =OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=BASE_URL,
    api_key= API_KEY,
    check_embedding_ctx_length=False 

)

def cosine_similarity(a:list[float], b: list[float]) -> float:
    """cos(theta) = (a . b)/ |a|. |b|"""
    dot= sum (x * y for x,y in zip(a,b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(y*y for y in b))
    return dot/(norm_a * norm_b) if norm_a and norm_b else 0.0 # 1= similar and 0=unrelated

#passages=[  
#    "Meridian home loan eligibility criteria requires a minimum credit score of 700",
#    "Savings accounts earn 3.0% interrest per anum",
#    "report a lost or stolern credit card immediately to avoid fraudulent charges"
#]

passages = [
    "Meridian home loan eligibility criteria requires a minimum credit score of 700",
    "Savings accounts earn 3.0% interest per annum",
    "Report a lost or stolen credit card immediately to avoid fraudulent charges",
]


query =" What credit score do I need to borrow a home loan"

passages_vector = embeddings.embed_documents(passages)
query_vector =embeddings.embed_query(query)

scored=[(cosine_similarity(query_vector,pv),p) for pv,p in zip(passages_vector,passages)]
scored.sort(reverse=True) # highest similarity first

print(f"query: {query}\n")

for score, passage in scored:
    print(f"{score:.4f} {passage}")

print(f"\nbest match->{scored[0][1]}")


# passages = [
#     "queen",
#     "king",
#     "prince",
#     "computer science"
# ]

# query = "princess"


# passages_vector = embeddings.embed_documents(passages)
# query_vector = embeddings.embed_query(query)

# scored = [(cosine_similarity(query_vector, pv), p) for pv, p in zip(passages_vector, passages)]
# scored.sort(reverse=True) # highest similarity first

# print(f"\nquery: {query}\n")
# for score, passage in scored:
#     print(f" {score:.4f} {passage}")

# print(f"\nbest match -> {scored[0][1]}")
