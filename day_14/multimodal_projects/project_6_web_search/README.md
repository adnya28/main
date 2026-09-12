# Project 6 — a model that can search the web

Not a modality — a **capability**. Nothing new goes into the message; the model simply gains the
ability to look something up. And there are two very different ways to buy it, both in this one
file — plus a checkbox that takes the capability away again, so the room can hear the difference.

```bash
uv run python chatbot.py
uv run python app.py
```

## Ask it

| Question | What should happen |
|---|---|
| *What is the RBI repo rate right now?* | a current number, with the date or source named |
| *What did the RBI announce at its most recent policy meeting?* | a summary no training set could contain |
| *What is today's USD to INR rate?* | ask twice a week apart; the answer moves |

Ask each one **twice — once with "Search the web" ticked, once unticked**. That contrast is the
whole lesson and it lands better than any slide. A real run on 2026-09-06:

| | Answer |
|---|---|
| unticked | *"As of my last update, the RBI repo rate is **6.50%**."* |
| ticked | *"currently **5.25%**"*, with rbi.org.in cited and the date given |

Same model, same question, ninety seconds apart. (Before the toggle existed you had to open
**project 1** to get the stale half; that still works, but one page is better theatre.)

## Talking points

- **Two ways to buy a capability, one file.**

  | `web_search` in `config.py` | Provider | Who searches | Code |
  |---|---|---|---|
  | `"native"` | OpenRouter | the *provider*, before the model reads anything | `ai.model + ":online"` — one suffix |
  | `"ddgs"` | Google AI Studio, Ollama | *you*, with `DDGS()`, pasted into the prompt | six lines |

  Google *does* have a grounding-with-Search tool — it is simply not exposed on the
  OpenAI-compatible endpoint, so here it takes the same path as the laptop.

  The second one is what the first one is doing for you. Once a class has seen `search()`,
  `:online` stops being magic and becomes a hosted convenience with a price tag.
- **This is RAG.** Retrieve, then generate — the identical shape as `../../rag/`, except the
  corpus is the internet instead of four PDFs. Say that out loud; students rarely connect them.
- **The toggle swaps the system prompt too**, not just the lookup. `GROUNDED` says *"answer from
  the search results only, and finish with the date or source"*; `FROM_MEMORY` says *"answer from
  what you already know, and say plainly if you may be out of date"*. Retrieval and the
  instruction to use it are two separate decisions — students tend to assume one implies the other.
- **"Finish with the date or source you relied on"** in `GROUNDED` is doing heavy lifting.
  Without it you cannot tell a searched answer from a remembered one.
- **The failure mode moved.** The model is no longer wrong from ignorance — it is now only as
  right as the pages it found. In a regulated setting, an allowlist of domains beats open search.

## Extend it

Restrict `search()` to `site:rbi.org.in` and you have the beginnings of a compliant assistant:
current, and sourced only from the regulator. Then hand the same function to a LangGraph agent as
a `@tool` (see `../../mcp_projects/project_1_langgraph_tool_agent`) and let the model decide
*whether* to search rather than always searching.
