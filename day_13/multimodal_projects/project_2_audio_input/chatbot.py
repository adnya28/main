"""
Multimodal LLMs - Project 2 - chatbot.py: AUDIO in, text out
--------------------------------------------------------------
Project 1 sent a string. This one sends a LIST of content parts, and one part
is a sound file. No separate speech-to-text step: the model that answers is the
model that listens.  Run:  python chatbot.py
"""

import base64                                                # turns the raw sound file into sendable text
from pathlib import Path                                     # to find question.mp3 sitting next to this file
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # config.py lives one folder up
from config import use, text_of

ai = use("openrouter")                                       # <- change this ONE word: openrouter | google | ollama
if not ai.audio:                                             # said plainly, rather than a raw 400 later
    raise SystemExit(f"{ai.model} cannot listen. Use openrouter or ollama for this project.")

SYSTEM = "You are Meridian Bank's assistant. First repeat what you heard, then answer it in two sentences."

def answer(audio_path: str, history: list | None = None) -> str:   # a FILE PATH in this time, not a sentence
    audio = Path(audio_path)
    data = base64.b64encode(audio.read_bytes()).decode()     # the bytes of the file, encoded as plain text
    reply = ai.client.chat.completions.create(model=ai.model, messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": [{"type": "input_audio", "input_audio": {   # a LIST of parts, not a string
            "data": data, "format": "mp3" if audio.suffix == ".mp3" else "wav"}}]}])   # the model must be told which
    return text_of(reply)                                    # strips any <thought> narration, handles None

if __name__ == "__main__":
    import sys
    clip = sys.argv[1] if len(sys.argv) > 1 else exit("Give me a sound file:  python chatbot.py myquestion.mp3")
    print(f"[{ai.label}]")
    print(answer(clip))