# Project 4 — an image in, text out

Same shape as project 2 with one part swapped: `input_audio` becomes `image_url`. That is the
whole diff, and showing the two files side by side is the fastest way to make "multimodal" click.

```bash
python ../make_samples.py    # writes rate_card.png, if you have not already
uv run python chatbot.py
uv run python app.py         # then drag any image in
```

## Ask it

| Image + question | What should happen |
|---|---|
| `rate_card.png` — *what is the car loan rate, and is a gold loan offered?* | **9.6%**, and *not offered* — both read off the picture |
| `rate_card.png` — *which product is most expensive to borrow?* | personal loan, 13.5% — it has to compare, not just read |
| `rate_card.png` — *what is the education loan rate?* | it should **refuse**; the row is not on the card |
| a photo of a real payslip or form | try it live — this is the demo that sells the technology |

## Talking points

- **A data URL is the whole image as one string.** `data:image/png;base64,iVBORw0…`. Nothing is
  uploaded to a file server; the picture *is* part of the prompt. Show them how long that string
  is — that is why image prompts cost real money.
- **The refusal is the feature.** The SYSTEM prompt says *answer only from what is visible*.
  Without it the model will happily invent an education loan rate. Grounding a vision model is the
  same discipline as grounding a RAG chatbot (see `../../rag/`).
- **"Reading a document" and "seeing an image" are the same call.** Screenshots, scans, whiteboard
  photos, handwriting, charts, a photograph of a broken machine — one API, no OCR library.
- **`gemma4:e2b` does this on the laptop.** Run it with `PROVIDER=ollama` and no image ever leaves
  the room. For a bank, that sentence is often the deciding one.

## Extend it

Change `SYSTEM` to *"Return only JSON with keys product and rate, one object per row"*, and you
have turned a photograph into a database record. That is document processing — the highest-value
boring use of vision models in enterprise.