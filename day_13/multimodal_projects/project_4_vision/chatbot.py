"""
Multimodal LLMs - Project 4 - chatbot.py: an IMAGE in, text out
----------------------------------------------------------------
Same shape as project 2 with one part swapped: input_audio becomes image_url.
The image travels inside the URL as base64 - nothing is uploaded anywhere.
Run:  python chatbot.py
"""

import base64, mimetypes                                     # mimetypes works out "image/png" from the file name
from pathlib import Path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # config.py lives one folder up
from config import use, text_of

ai = use("openrouter")                                       # <- change this ONE word: openrouter | google | ollama
SYSTEM = "Answer only from what is visible in the image. If it is not shown, say so - never guess a number."

def answer(image_path: str | None, question: str) -> str:    # a picture and a question about it
    if not image_path:                                       # Gradio sends None if you press Submit with no image
        return "Upload or drag in an image first, then press Submit."
    data = base64.b64encode(Path(image_path).read_bytes()).decode()
    url = f"data:{mimetypes.guess_type(image_path)[0]};base64,{data}"   # a "data URL" - the whole image as one string
    reply = ai.client.chat.completions.create(model=ai.model, messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": [{"type": "text", "text": question},          # part 1: the words
                                     {"type": "image_url", "image_url": {"url": url}}]}])   # part 2: the picture
    return text_of(reply)                                    # strips any <thought> narration, handles None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        exit('Give me an image:  python chatbot.py photo.png "What does this say?"')
    question = sys.argv[2] if len(sys.argv) > 2 else "What is in this image?"
    print(f"[{ai.label}]")
    print(answer(sys.argv[1], question))