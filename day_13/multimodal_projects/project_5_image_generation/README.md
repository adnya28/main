# Project 5 — text in, an image out

Every project so far added a modality on the way **in**. This one adds it on the way **out**, and
the call barely changes: ask for the `image` modality, and the reply carries a picture.

**This project always uses OpenRouter**, whatever the other six are set to:

```python
ai = use("openrouter")     # pictures always come from OpenRouter
```

Not preference — arithmetic:

| Provider | Can it make a picture? |
|---|---|
| OpenRouter | yes — `google/gemini-2.5-flash-image`, about $0.00003 each |
| Google AI Studio | free tier allows **`limit: 0`** image requests. A paid key would work. |
| Ollama | no image models exist for it |

So set every other project to `use("ollama")` and run the whole class offline — except this one.
That is the honest edge of portability, and it is worth saying out loud.

```bash
uv run python chatbot.py     # writes generated.png next to the script
uv run python app.py
```

## Ask it

| Prompt | What should happen |
|---|---|
| *A clean flat-style icon of a house with a rupee coin beside it, for a home loan web page.* | a usable icon, plus a sentence of caption |
| *A simple line-art illustration of a bank branch, plain white background.* | note how much the words "plain white background" change the result |
| *A rate card table showing home 8.4%, car 9.6%, personal 13.5%* | it will look right and **be wrong** — image models cannot spell reliably |

## Talking points

- **`modalities: ["image", "text"]`** is the entire request. Same endpoint, same SDK, same message
  list as project 1 — only what you asked to receive changed.
- **The picture comes back as base64 inside the reply**, exactly like the image *went out* in
  project 4. Same encoding, opposite direction; `chatbot.py` splits the header off and writes real
  PNG bytes.
- **Text inside generated images is unreliable.** Run the third prompt and read the numbers aloud.
  This is the single most common way a demo embarrasses somebody in front of a client.
- **Governance.** Generated imagery in a regulated industry needs provenance, brand review and a
  usage policy before it goes anywhere near a customer. Worth two minutes in a banking room.

## Extend it

Pass an image *in* alongside the prompt and ask for one *out* — that is editing, not generation:
*"make this rate card's background navy and the text white"*. Projects 4 and 5 in a single call.