import asyncio, os, sys
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()
model=os.environ["MODEL"]
SEVERS = {"loans": {"command":sys.executable,
                    "args": [str(Path(__file__).parent / "server.py")],
                    "transport": "stdio"}}

async def anwser(message:str, history: list | None = None) -> str:
    tools =await MultiServerMCPClient(SEVERS).get_tools()
    agent= create_agent(
        init_chat_model(model=model, model_provider="openrouter"),
        tools=tools,
        system_prompt="Ypu are Meridian Book's Laon assistant.")
    result = await agent.ainvoke({"messages": [{"role": "user", "content": message}]})
    return result["messages"][-1].content
    

if __name__ == "__main__":
    print(asyncio.run(anwser("What is the EMI on a 500,000 home loan for 20 years?")))