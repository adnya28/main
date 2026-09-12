"""
Multimodal LLMs - Project 3 - chatbot.py: audio in, AUDIO out
--------------------------------------------------------------
"Speech to speech" is nearly always two models in a row: one that listens and
answers, and one that speaks the answer. This file is project 2 plus a mouth.
Run:  python chatbot.py
"""

import base64
from pathlib import Path
from gtts import gTTS                                        # the mouth: free text-to-speech, no key, needs internet
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # config.py lives one folder up
from config import use, text_of

ai = use("openrouter")                                       # <- change this ONE word: openrouter | google | ollama
if not ai.audio:                                             # said plainly, rather than a raw 400 later
    raise SystemExit(f"{ai.model} cannot listen. Use openrouter or ollama for this project.")

SYSTEM = "You are Meridian Bank's phone assistant. Reply in ONE short spoken sentence - no lists, no symbols."

def answer(audio_path: str | None) -> tuple[str, str | None]:   # sound in, and BOTH the words and the sound back out
    if not audio_path:                                       # Gradio sends None if you press Submit with nothing recorded
        return "Record something with the microphone first, then press Submit.", None
    audio = Path(audio_path)
    data = base64.b64encode(audio.read_bytes()).decode()     # exactly as project 2 - the ears half of this file
    reply = text_of(ai.client.chat.completions.create(model=ai.model, messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": [{"type": "input_audio", "input_audio": {
            "data": data, "format": "mp3" if audio.suffix == ".mp3" else "wav"}}]}]))
    reply = reply or "Sorry, I did not catch that."          # gTTS cannot speak nothing
    spoken = str(Path(__file__).parent / "reply.mp3")        # overwritten every turn - it is a scratch file
    gTTS(reply).save(spoken)                                 # the second model: text back into sound
    return reply, spoken                                     # the text is shown, the file is played

if __name__ == "__main__":
    import sys
    clip = sys.argv[1] if len(sys.argv) > 1 else exit("Give me a sound file:  python chatbot.py myquestion.mp3")
    print(f"[{ai.label} + gTTS]")
    print(answer(clip))