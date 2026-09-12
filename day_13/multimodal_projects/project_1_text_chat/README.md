# Project 1 — text in, text out

The baseline, and deliberately the *least* interesting file here. Read it once and you have read
80% of every other project in this folder.

```bash
uv run python chatbot.py     # one worked example in the terminal
uv run python app.py         # the same thing as a chat page
```

## Ask it

| Question | What should happen |
|---|---|
| *What is an EMI?* | a two-sentence definition |
| *Explain a floating interest rate to a first-time borrower.* | plain language, no jargon |
| *What is the car loan rate at Meridian Bank?* | it has no idea — watch it either refuse or invent one |

That last row is the point of projects 4, 6 and 7: the model only knows what it was trained on,
until you give it eyes, a search box, or your data.

## Talking points

- **The line that changes.** `{"role": "user", "content": message}` — `content` is a **string**.
  In every other project it becomes a **list**. Nothing else about the call moves.
- **One SDK, two providers.** `PROVIDER=ollama` in `../../.env` points the same code at your
  laptop. Run it both ways in front of the class; the code does not change, only the address.
- **Modal vs model vs modality.** A *model* is the network. A *modality* is a kind of data.
  *Multimodal* means several kinds. ("Modal" on its own, in web development, is a pop-up box —
  a different word entirely.)

## Extend it

`answer()` throws the conversation away after every turn — `history` arrives and is ignored. Feed
it back in as extra messages and the chatbot gains a memory. Compare with
`module_01_llm_mechanics_openai_setup/05_chatbot_with_memory.py`, which does exactly that.