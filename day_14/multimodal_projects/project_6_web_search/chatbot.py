"""
Multimodal LLMs - Project 6 - chatbot.py: a model that can SEARCH THE WEB
--------------------------------------------------------------------------
Not a new modality - a new capability, and there are two ways to buy it.
OpenRouter sells it: append ":online" and the provider searches for you.
Everyone else: we search ourselves and paste the results in. config.py says
which, per provider. The toggle turns lookup OFF, so you can hear the
difference between a model that searched and one answering from memory.
Run:  python chatbot.py
"""

from ddgs import DDGS                                        # DuckDuckGo search, no API key needed
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # config.py lives one folder up
from config import use, text_of

ai = use("openrouter")                                       # <- change this ONE word: openrouter | google | ollama
GROUNDED    = "Answer from the search results only, and finish with the date or source you relied on."
FROM_MEMORY = "Answer from what you already know. Say plainly if your answer may be out of date."

def search(query: str, n: int = 5) -> str:                   # OUR search tool - this is what ":online" does for you
    return "\n".join(f"- {r['title']}: {r['body']}" for r in DDGS().text(query, max_results=n))

def answer(message: str, history: list | None = None, search_on: bool = True) -> str:
    if not search_on:                                        # toggle OFF - no lookup at all, training memory only
        model, prompt, system = ai.model, message, FROM_MEMORY
    elif ai.web_search == "native":                          # the provider searches BEFORE the model reads anything
        model, prompt, system = ai.model + ":online", message, GROUNDED
    else:                                                    # we fetch the pages ourselves and hand them over
        model, prompt, system = ai.model, f"Search results:\n{search(message)}\n\nQuestion: {message}", GROUNDED
    return text_of(ai.client.chat.completions.create(model=model, messages=[    # text_of drops <thought> narration
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}]))

if __name__ == "__main__":
    q = "What is the RBI repo rate right now?"               # a question no model can know from training alone
    print(f"[{ai.label} | search: {ai.web_search}]")
    print("SEARCH OFF:", answer(q, search_on=False), "\n")   # the same question both ways - that IS the demo
    print("SEARCH ON :", answer(q, search_on=True))
