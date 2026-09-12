# Project 3b — a real phone call: Gemini Live, FastAPI and React

Projects 3 and 3a still **took turns**: you spoke, it waited, it answered. Even 3a, with one model
doing both halves, was a request and a response — and it sounded like one.

3b holds a **call**. One websocket stays open, audio flows both ways at once, Gemini decides when
you have stopped talking, and **you can cut it off mid-sentence and it stops**. That last part is
what makes it sound human, and it is impossible in a request/response design.

```bash
./run.sh                    # installs, builds and serves - then open http://127.0.0.1:8000
```

`run.sh` stops an older copy of this same server if one is still holding the port (the usual way a
second run fails), and refuses politely if the port belongs to something else. `PORT=8010 ./run.sh`
moves it.

or the three steps it wraps:

```bash
cd web && npm install && npm run build && cd ..
uv run python server.py     # http://127.0.0.1:8000   (Chrome, not the VS Code browser)
```

Working on the UI? `cd web && npm run dev` gives hot reload on `:5173` and forwards the websocket
to `server.py`, so run both.

## What changed, and why it sounds different

| | 3 — pipeline | 3a — native turn | **3b — live** |
|---|---|---|---|
| Models per answer | 2 (listen, then gTTS) | 1 | 1 |
| Turn-taking | you press Submit | our own loudness maths | **the model's own VAD** |
| Interrupt it? | no | no | **yes — just talk over it** |
| Transport | HTTP request | HTTP request | **one open websocket** |
| Transcript of *you* | none | none | **yes, as a courtesy** |
| Provider | any | OpenRouter | Google AI Studio |
| Front end | Gradio | Gradio | **React + TypeScript** |

Gemini's native-audio models do not turn your voice into text, think, then read an answer out.
They work in sound the whole way through, which is why pace, emphasis and hesitation survive.

## The four files that matter

### `server.py` — a bridge, and almost nothing else (~60 lines)

```
browser  --16kHz PCM-->  server.py  -->  Gemini Live
browser  <--24kHz PCM--  server.py  <--  Gemini Live
```

Two `async` loops copying bytes in opposite directions at the same time. There is **no** silence
detection, no chunking, no turn management — the model does all of it, which is precisely why this
file is so much smaller than 3a's. Note the two fixed rates: Live takes **16 000 Hz** in and always
returns **24 000 Hz** out.

The API key never reaches the browser. That is the whole reason a backend exists here at all.

### `web/public/pcm-worklet.js` — the microphone, on the audio thread

An `AudioWorkletProcessor` runs on the browser's real-time audio thread, so a busy React render
can never stutter the microphone. It gathers the browser's tiny 128-sample blocks into 100ms
parcels and posts them to the page.

### `web/src/live.ts` — all the audio, none of the interface

Converts float samples to PCM16, streams them up, and queues the reply so the pieces play back
seamlessly (`playHead` schedules each buffer to start exactly where the last one ended).

**The most important three words in this project are `echoCancellation: true`.** Without it the
microphone hears the assistant, the assistant hears itself, and it interrupts itself forever.
Project 3a solved that by going deliberately deaf while speaking — which also made interruption
impossible. The browser's echo canceller is what lets 3b listen and speak at the same time.

When the server forwards `interrupted`, `stopSpeaking()` throws away every buffer not yet played.
That is barge-in, and it is four lines.

### `web/src/App.tsx` — the interface, and no audio at all

Same split as every other project here: `app.py` holds no model logic, `App.tsx` holds no audio
logic. The orb scales with the live microphone level, so the page shows you it can hear you
without printing a number.

## Ask it

| Try this | What should happen |
|---|---|
| *"What is the interest rate on a home loan?"* | a natural spoken sentence, and both sides appear in the transcript |
| **interrupt it halfway through an answer** | it stops instantly — this is the demo |
| *"What would my monthly payment be on a 50 lakh home loan at 8.4% over 25 years?"* | about **Rs.39,918** — against a true EMI of Rs.39,924.97 |
| *"And for a car loan instead?"* | it remembers; the session holds the whole call |

That EMI is worth pausing on in class. Project 3a answered the same question with *"around 42,000
to 43,000"*. Both are guesses rather than calculations — 3b's is simply a much better guess. **The
honest fix is still a tool**, exactly as in `mcp_projects/project_1`; a model that sounds more
confident is not a model that can do arithmetic.

## Talking points

- **Count the round trips.** 3a: record, upload, wait, download, play. 3b: one connection, opened
  once, with audio moving both ways continuously. That is the entire difference in feel.
- **The backend got smaller as the product got better.** Everything 3a's `chatbot.py` did by hand —
  detecting silence, ending turns, suppressing echo — is either the model's job or the browser's.
  Worth showing side by side.
- **Two transcripts that change nothing.** `input_audio_transcription` and
  `output_audio_transcription` exist purely for the screen. Turn them off and the assistant behaves
  identically — proof that no text step is in the loop.
- **Why a backend at all?** The browser could open a websocket to Google directly, and then the API
  key would be in the page source for anyone to read. `server.py` exists to hold the key, and in
  production it would also hold auth, logging and rate limits.
- **This is the one project that needs Google.** OpenRouter has no Live endpoint, and no local
  model does bidirectional audio. `config.py` records that as `"voice_model": None` for the
  others — 3b does not use `config.py` at all, because the Live API is a different SDK
  (`google-genai`) and a different wire format from the OpenAI-compatible endpoint the other seven
  projects share.

## Setup

Only `GOOGLE_API_KEY` in the `.env` (the AI Studio key, **not** the OAuth values project 7 uses).
Node 20+ and npm for the front end.

Voices: `Aoede`, `Puck`, `Charon`, `Kore`, `Fenrir`, `Leda`, `Orus`, `Zephyr` — change `VOICE` at
the top of `server.py`. Models: `gemini-2.5-flash-native-audio-latest` is the most natural;
`gemini-3.1-flash-live-preview` is faster and also works.

**Open it in Chrome.** The VS Code built-in browser is never granted microphone access and fails
silently, and `getUserMedia` needs a secure context — `127.0.0.1` counts, a LAN IP does not.
