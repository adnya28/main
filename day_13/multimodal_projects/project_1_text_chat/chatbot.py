"""
Multimodal LLMs - Project 1 - chatbot.py: text in, text out
------------------------------------------------------------
The baseline, and the only project here that is NOT multimodal. Every other
project is this file plus one new kind of content.  Run:  python chatbot.py
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # config.py lives one folder up
from config import use, text_of

ai = use("openrouter")                                       # <- change this ONE word: openrouter | google | ollama
SYSTEM = "You are Meridian Bank's assistant. Answer in two sentences at most."

def answer(message: str, history: list | None = None) -> str:   # one question in, one reply out (Gradio sends history)
    reply = ai.client.chat.completions.create(model=ai.model, messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": message}])               # content is a plain STRING - this is the line that changes
    return text_of(reply)                                    # strips any <thought> narration, handles None

if __name__ == "__main__":
    print(f"[{ai.label}]")                                   # so you always know which model just answered
    print(answer("What is an EMI, in one sentence?"))