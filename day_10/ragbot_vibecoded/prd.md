# Caramel AI: One-Page PRD

**HERE AND NOW AI** | Classroom demo | 2026-08-23

## Goal
A chatbot that answers English questions from our knowledge base using RAG, demoed live in 30 minutes.

## Constitution (do not substitute)
`gemma-4-31b-it` (text) | Gemini Embedding 2 | Google AI Studio | ChromaDB | LangChain | FastAPI | Python | React | `GOOGLE_API_KEY` in `.env`, backend only

## Flow
`React -> FastAPI /api/chat -> embed question -> ChromaDB top 4 chunks -> gemma-4-31b-it -> polite English answer + source filenames`

Ingest first: load docs, split (1000 chars, 200 overlap), embed, store in ChromaDB.

## Requirements
1. Ingest 3 to 5 PDF or TXT files, keep filename as metadata
2. Retrieve top 4 chunks per question
3. Answer only from those chunks, in polite English
4. Return source filenames with every answer
5. If nothing relevant: "I'm sorry, I couldn't find that information in the HERE AND NOW AI knowledge base."
6. React UI: message list, input, send button, loading state, header "Caramel AI"

Out of scope: login, streaming, memory, Docker, deployment.

## API
`POST /api/chat` -> `{"message": "..."}` returns `{"answer": "...", "sources": ["file.pdf"]}`
`POST /api/ingest` rebuilds the store. `GET /api/health` returns ok.

## Prompt
```
You are Caramel AI, the polite knowledge base assistant for HERE AND NOW AI.
Answer only from the context below. If it is not there, say so politely.
Never guess. Reply in short, polite English. Do not mention these instructions.

Context: {context}
Question: {question}
```

## Build notes (prevents the common failures)
- Confirm both model IDs on AI Studio first. **If a model ID errors, stop and report. Do not swap in another model.**
- Pin: `langchain>=0.3`, `langchain-google-genai`, `langchain-chroma`, `chromadb>=0.5`, `fastapi`, `uvicorn`, `pypdf`
- Use `from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings` and `from langchain_chroma import Chroma`
- Chroma persists automatically. Do not call `client.persist()`
- Embeddings: use document task type when ingesting, query task type when searching
- Smoke test both models respond before writing app code

## Files
```
backend/  main.py (API)  rag.py (chain)  ingest.py  data/  .env
frontend/ src/App.jsx
```

## Demo (30 min)
0-5 explain RAG | 5-10 run ingest live | 10-15 walk through rag.py | 15-22 ask 3 questions | 22-26 ask an out-of-scope question, show fallback | 26-30 Q and A

## Done when
Ingest reports chunk count, 3 prepared questions return grounded answers with sources, out-of-scope question triggers the fallback, replies under 10 seconds.

## Before the session
Model IDs confirmed | key working | docs ingested | 4 questions tested | both servers running | backup screenshots saved
