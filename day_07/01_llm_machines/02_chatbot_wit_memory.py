import os
from openai import OpenAI
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()

base_url = os.environ["BASE_URL"]
api_key = os.environ["OPENROUTER_API_KEY"]
MODEL = os.environ["MODEL"]

client = OpenAI(base_url=base_url, api_key=api_key)

SYSTEM_PROMPT = "You are a friendly assistant. Answer in one or two short sentences."

messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": SYSTEM_PROMPT}]

print("\n Chatbot with Memory. Try : 'My name is Adnya'")

print("Type 'quit' to exit the chatbot.")

while True:
    user_input=input("You:").strip()

    if not user_input:
        continue
    if user_input.lower() in ("quit", "exit"):
        print("Exiting the chatbot. Goodbye!")
        break

    #1. Add the human's new question to the END
    messages.append({"role":"user", "content":user_input})

    response=client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    reply= response.choices[0].message.content or ""

    #2. add the AI's own answer to transcript too
    messages.append({"role":"assistant","content":reply})
    print(f"Caramel AI:, {reply} \n") 