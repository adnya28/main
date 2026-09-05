import asyncio, os, sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()
model=os.environ["MODEL"]

TOKEN=os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
SERVERS = {"github": {"url": "https://api.githubcopilot.com/mcp/",
                    "transport": "streamable_http",
                    "headers": {"Authorization": f"Bearer {TOKEN}"}}}

ALLOWED={"get_me", "search_respositories","get_file_contents",
         "create_repository","create_or_update_file"}

async def anwser(message:str, history: list | None = None) -> str:
    tools =await MultiServerMCPClient(SERVERS).get_tools()
    agent= create_agent(
        init_chat_model(model=model, model_provider="openrouter"),
        tools=tools,
        system_prompt="You are github copilot assistant.")
    result = await agent.ainvoke({"messages": [{"role": "user", "content": message}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    print(asyncio.run(anwser("Who am I on Github and how many public repositories do I have")))
