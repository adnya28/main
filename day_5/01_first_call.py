import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(base_url=os.environ["BASE_URL"], api_key=os.environ["OPENROUTER_API_KEY"])

MODEL = os.environ["MODEL"]

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a Tax Consultant assistant. Always answer in a few lines."},
        {"role": "user", "content": "How can i reduce my tax liability"}
    ]
)

print("Caramel AI: ", response.choices[0].message.content)

