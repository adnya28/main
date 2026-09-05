import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool

load_dotenv()
model=os.environ["MODEL"]

RATES= {"home":8.4, "car":9.5, "personal":12.5,"business":12.5}

@tool
def get_rate(product:str) -> float:
    """Today's annual interrest rate is % for 'home' , 'car', 'personal', 'business'."""
    return RATES.get(product.lower(),0.0)

@tool
def calculate_emi(principal:float, annual_rate:float,years:int) -> float:
    """Monthly emi in USD foa a loan amount for annual rate in %  and a tenure in years"""
    r,n = annual_rate/1200 , years *12
    return round(principal * r*(1+r) ** n/((1+r) ** n-1),2)

agent = create_agent(
    init_chat_model(model =model, model_provider="openrouter"),
    tools=[get_rate,calculate_emi],
    system_prompt="Ypu are Meridian Book's Laon assistant."
)

def answer(message:str, history:list | None =None) ->str:
    return agent.invoke({"messages":[{"role":"user", "content":message}]})["messages"][-1].content

if __name__ == "__main__":
    print(answer("what is the emi on 500,000 home loan for 20 years?"))
