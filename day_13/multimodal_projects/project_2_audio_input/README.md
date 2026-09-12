# Project 2 — audio in, text out

The first genuinely multimodal project. There is **no speech-to-text step**: the sound file goes
straight to the model that answers it.

```bash
python ../make_samples.py    # writes question.mp3, if you have not already
uv run python chatbot.py
uv run python app.py         # then use the microphone
```

## Ask it

| Try this | What should happen |
|---|---|
| the supplied `question.mp3` | it repeats the question back, then answers it |
| the same question, spoken live into the mic | same answer — accents and pauses and all |
| a question in Tamil or Hindi | most modern models answer in the language you used |
| deliberate background noise | watch what it mishears; this is where voice products fail |

## Not every model can listen

`use("google")` will stop with *"gemma-4-31b-it cannot listen"*. Gemma is a text-and-vision model;
Google's OpenAI-compatible endpoint answers `400 Audio input modality is not enabled for this
model`. `config.py` records that as `"audio": False` so the project refuses in one sentence rather
than throwing an HTTP error at the class.

Use `openrouter` or `ollama` here. Checking `ollama show <model>` for an `audio` capability before
assuming is the habit worth teaching.

## Talking points

- **`content` became a list.** That is the entire change from project 1:

  ```python
  "content": [{"type": "input_audio", "input_audio": {"data": <base64>, "format": "mp3"}}]
  ```

  A message is not a sentence. It is a list of parts, and each part has a type.
- **base64** turns raw bytes into ordinary characters so they can travel inside JSON. It costs
  about 33% extra size — which is why audio and image prompts are expensive.
- **Nothing was uploaded anywhere.** There is no file server; the sound *is* the prompt.
- **Which models can listen?** Not many. `gemma4:e2b` reports `audio` in `ollama show`;
  `google/gemini-2.5-flash` does it in the cloud. Ask the class to check before assuming.

## Extend it

Change `SYSTEM` to ask for JSON — `{"intent": ..., "product": ..., "amount": ...}` — and you have
the front end of a voice IVR that routes callers, in about twenty lines.