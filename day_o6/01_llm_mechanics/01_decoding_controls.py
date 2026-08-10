import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(base_url=os.environ["BASE_URL"], api_key=os.environ["OPENROUTER_API_KEY"])

#MODEL = os.environ["MODEL"]
MODEL = "google/gemini-3-flash-preview" #"google/gemini-2.5-flash-lite" #"google/gemini-3.6-flash"

PROMPT= "Give a name for a new savings account product. Reply with just the name."

def generate(temparature: float = 0.7, max_tokens: int = 20, stop=None) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": PROMPT}
        ],
        temperature=temparature,
        top_p=1.0,
        max_tokens=max_tokens,
        stop=stop
    )
    return (response.choices[0].message.content or "").strip()
#.strip()

print("=== temperature 0.0 (run 3x = expect near identical outputs) ===")
for _ in range(3):
    print(generate(0.0))

print("\n=== temperature 2.0 (run 3x = expect some variation) ===")
for _ in range(3):
    print(generate(2.0))

print("=== max tokens=1 (truncate output) ===")
#for _ in range(3):
print(generate(0.7, max_tokens=1))
