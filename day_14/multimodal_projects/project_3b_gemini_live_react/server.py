"""
Multimodal LLMs - Project 3b - server.py: a bridge, and almost nothing else
----------------------------------------------------------------------------
Project 3a still took turns: record, wait, answer. This one holds a CALL. The
browser opens one websocket and keeps it open; audio flows both ways at the
same time; Gemini decides when you have stopped talking, and you can cut it off
mid-sentence and it stops.

That is why the backend is so small. It does not chop up audio, detect silence
or manage turns - the model does all of it. This file only copies bytes:

    browser  --16kHz PCM-->  this file  -->  Gemini Live
    browser  <--24kHz PCM--  this file  <--  Gemini Live

Run:  uv run python server.py        then open http://127.0.0.1:8000
"""

import asyncio, os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types

load_dotenv()                                                # the .env with GOOGLE_API_KEY, found by walking up
HERE = Path(__file__).parent
DIST = HERE / "web" / "dist"                                 # the built React app, if it has been built

MODEL = "gemini-2.5-flash-native-audio-latest"               # native audio: it thinks IN sound, it does not read out text
VOICE = "Aoede"                                              # Puck, Charon, Kore, Fenrir, Aoede, Leda, Orus, Zephyr
MIC_RATE, SPEAKER_RATE = 16000, 24000                        # Gemini Live is fixed at these two: 16k in, 24k out
SYSTEM = ("You are Meridian Bank's phone assistant, on a live phone call. Speak the way a person "
          "speaks: one or two short sentences, no lists, no symbols, no markdown. If you need a "
          "number from the caller, just ask for it.")

if not os.getenv("GOOGLE_API_KEY"):
    raise SystemExit("GOOGLE_API_KEY is not set in the .env - get one at https://aistudio.google.com/apikey")

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
CONFIG = types.LiveConnectConfig(
    response_modalities=[types.Modality.AUDIO],              # it answers in sound, never in text
    system_instruction=SYSTEM,
    speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(
        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=VOICE))),
    input_audio_transcription=types.AudioTranscriptionConfig(),    # a transcript of YOU, for the screen only
    output_audio_transcription=types.AudioTranscriptionConfig(),   # ...and of it. Neither is in the loop.
)

app = FastAPI(title="Project 3b - Gemini Live")


@app.websocket("/ws")
async def call(browser: WebSocket):
    """One websocket = one phone call. Two copy loops running at the same time."""
    await browser.accept()
    try:
        async with client.aio.live.connect(model=MODEL, config=CONFIG) as live:
            await browser.send_json({"event": "ready", "model": MODEL, "voice": VOICE})

            async def microphone_to_model():
                while True:
                    message = await browser.receive()
                    if message["type"] == "websocket.disconnect":
                        return
                    if chunk := message.get("bytes"):         # raw PCM16 straight off the microphone
                        await live.send_realtime_input(
                            audio=types.Blob(data=chunk, mime_type=f"audio/pcm;rate={MIC_RATE}"))

            async def model_to_speaker():
                # live.receive() delivers exactly ONE turn and then ends - read its source if you
                # doubt it. So ask for a new one each time, or the call goes silent after the first
                # answer and the microphone streams into nothing.
                while True:
                    anything = False
                    async for reply in live.receive():
                        anything = True
                        if reply.data:                        # its voice, in pieces, as it is spoken
                            await browser.send_bytes(reply.data)
                        said = reply.server_content
                        if not said:
                            continue
                        if said.input_transcription and said.input_transcription.text:
                            await browser.send_json({"role": "you", "text": said.input_transcription.text})
                        if said.output_transcription and said.output_transcription.text:
                            await browser.send_json({"role": "bank", "text": said.output_transcription.text})
                        if said.interrupted:                  # you talked over it - drop what it was saying
                            await browser.send_json({"event": "interrupted"})
                        if said.turn_complete:
                            await browser.send_json({"event": "turn_complete"})
                    if not anything:
                        return                                # the session really did close - do not spin

            await asyncio.gather(microphone_to_model(), model_to_speaker())
    except (WebSocketDisconnect, asyncio.CancelledError):
        pass                                                  # the caller hung up; nothing to clean up
    except Exception as error:
        print(f"[3b] call ended: {type(error).__name__}: {error}")


if DIST.exists():
    app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")

    @app.get("/pcm-worklet.js")
    async def worklet():
        return FileResponse(DIST / "pcm-worklet.js", media_type="text/javascript")

    @app.get("/")
    async def index():
        return FileResponse(DIST / "index.html")
else:
    @app.get("/")
    async def build_me():
        return HTMLResponse("<h2>The React app is not built yet</h2>"
                            "<pre>cd web &amp;&amp; npm install &amp;&amp; npm run build</pre>"
                            "<p>...then reload. Or run <code>npm run dev</code> for the hot-reloading version.</p>")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))                    # PORT=8010 python server.py, if 8000 is taken
    print(f"[3b] {MODEL}, voice {VOICE}  ->  http://127.0.0.1:{port}")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
