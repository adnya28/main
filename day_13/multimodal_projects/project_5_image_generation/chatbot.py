"""
Multimodal LLMs - Project 5 - chatbot.py: text in, an IMAGE out
----------------------------------------------------------------
Until now the new modality arrived on the way IN. Here it leaves on the way OUT,
and the call barely changes: ask for the image modality, and the reply carries
a picture.

This is the one project that does not follow the others' provider, because
image generation is not portable: Google's FREE tier allows zero pictures and
Ollama has no image model at all.  Run:  python chatbot.py
"""

import base64
from pathlib import Path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # config.py lives one folder up
from config import use

ai = use("openrouter")                                       # pictures always come from OpenRouter - see above
if not ai.image_model:
    raise SystemExit(f"{ai.name} has no image model in config.py. Use openrouter for this project.")

def answer(prompt: str) -> tuple[str, str]:                  # a description in, a caption and a PNG path out
    message = ai.client.chat.completions.create(model=ai.image_model, messages=[{"role": "user", "content": prompt}],
                                                extra_body={"modalities": ["image", "text"]}).choices[0].message
    images = message.model_dump().get("images") or exit("The model returned no image - try a plainer prompt.")
    data = images[0]["image_url"]["url"].split(",", 1)[1]    # strip the "data:image/png;base64," header off the front
    out = str(Path(__file__).parent / "generated.png")       # overwritten every turn - it is a scratch file
    Path(out).write_bytes(base64.b64decode(data))            # base64 text back into real PNG bytes
    return message.content or "", out                        # some models caption the picture, some say nothing

if __name__ == "__main__":
    print(f"[{ai.name}: {ai.image_model}]")
    print(answer("A clean flat-style icon of a house with a rupee coin beside it, for a home loan web page."))