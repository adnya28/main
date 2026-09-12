# Project 3 — audio in, audio out

The one everybody asks for: *"can I just talk to it?"* Yes — and it is worth seeing how the trick
is done, because it is almost never one model.

```bash
python ../make_samples.py
uv run python chatbot.py
uv run python app.py         # speak, then listen; the reply plays itself
```

## Ask it

| Try this | What should happen |
|---|---|
| the supplied `question.mp3` | one short spoken sentence back, played automatically |
| *"I earn ninety thousand a month, can I afford a fifty lakh home loan?"* | a short spoken answer |
| a long rambling question | notice the SYSTEM prompt forces a **short** reply — spoken text has different rules from written text |

## Not every model can listen

`use("google")` will stop with *"gemma-4-31b-it cannot listen"*. Gemma is a text-and-vision model;
Google's OpenAI-compatible endpoint answers `400 Audio input modality is not enabled for this
model`. `config.py` records that as `"audio": False` so the project refuses in one sentence rather
than throwing an HTTP error at the class.

Use `openrouter` or `ollama` here. Checking `ollama show <model>` for an `audio` capability before
assuming is the habit worth teaching.

## Talking points

- **Count the models.** There are two. `gemma4:e2b` (or Gemini) listens and decides what to say;
  `gTTS` says it. The text box in the middle of the page is the seam between them, exposed on
  purpose.
- **This is why voice assistants mishear you.** The mistake usually happens in the first model,
  before the clever one ever sees your words. Show it: mumble, and watch the transcript go wrong
  while the answer stays confidently fluent.
- **Latency adds up.** Listen → think → speak means three waits in a row. That is the reason
  production voice products stream each stage instead of waiting for the one before it to finish.
- **True end-to-end speech models exist** — OpenAI's `gpt-4o-realtime`, Gemini Live. One model,
  audio in and audio out, no text in between, so tone and interruptions survive. They need a
  websocket session and a direct provider key (OpenRouter does not proxy them), which is why this
  project uses the pipeline instead. Say that out loud in class; the pipeline is the honest
  starting point, not the state of the art.
- **`gTTS` needs the internet** even when the model is local. If you want the whole thing offline,
  swap it for `pyttsx3`, which uses your operating system's built-in voice.

## Extend it

`reply.mp3` is overwritten every turn. Keep them numbered and you have a transcript of the call in
both text and audio — which is exactly what a contact-centre product ships.