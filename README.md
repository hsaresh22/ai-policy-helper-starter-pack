 # AI Policy & Product Helper RAG

## A local-first RAG starter with **FastAPI** (backend), **Next.js** (frontend), and **Qdrant** (vector DB). Runs with one command using Docker Compose.

Tested on docker environment with OpenRouter. This is my first AI project, and it really piqued my interest on engineering with AI LLM models. 

I had to understand Vector Databases(so powerful), RAG, FastAPI and LLM Apis in a very short time. 

Because there is a time crunch for this assesment, I can only run through the essentials to meet the project acceptance criteria 

## Features and Fixes
- Fix docker compose, backend and frontend build errors
-------------------
- Extended rag.py with OpenRouter class
- Added OpenRouter envs in .env.example
- Updated docker-compose/backend to retrieve env vars
- Added requests HTTP client library to requirements.txt
- Added openrouter key & api env retrieval to settings.py
- Bugfix: convert metadata hash strings to numeric IDs in Qdrant upsert in rag.py
- added OpenRouterLLM class to rag.py
- updated LLM selection to include openrouter in rag.py
---------------------
- added ask-stream controller to enable stream functionality in main.py
- added generate_stream() to stream response from LLM
- add api apiAskStream to api.ts to call backend api and parse data
- add functionality for Chat.tsx to receive stream data and update chat
- Update Chat.tsx to show citations in organized lists
- Update Chat.tsx to add auto-scroll when messages update
------------------------
- Generate unit test for backend and frontend services
- Generate README for tests

## Architecture
Attached AI Policy Helper Application Architecture.pdf at root folder, please check

## Trade-offs?
For me this is bleeding-edge tech. At the moment I am unable to find any trade offs. Hoping in the future there will be a need to fine tune it so the app can be more efficient. But at the moment, this is a small tool and I dont see and specific flaws. 

The code does seem to get a little messy though, coming from a Java background and I wish there was better segregation of concerns I could put in place

The UI can definitely be a little prettier ;D

## What I'd ship next?
This tool has strong potential. I would expand it to include the full body of national laws e.g., Malaysia; and enable both legal professionals and the general public to query scenarios or cases and receive AI-assisted guidance with relevant citations. This would accelerate legal research and improve productivity, helping identify potential legal breaches or determine whether parties are protected under the law.

## Quick start / Setup

1) **Copy `.env.example` → `.env`** and edit as needed.

1.1) Run npm i in /frontend

2) **Run everything**:
```bash
docker compose up --build
```
- Frontend: http://localhost:3000  
- Backend:  http://localhost:8000/docs  
- Qdrant:   http://localhost:6333/dashboard#/welcome  (UI)

3) **Ingest sample docs** (from the UI Admin tab) or:
```bash
curl -X POST http://localhost:8000/api/ingest
```

4) **Ask a question**:
```bash
curl -X POST http://localhost:8000/api/ask -H 'Content-Type: application/json' \
  -d '{"query":"What’s the shipping SLA to East Malaysia for bulky items?"}'
```

## Offline-friendly
- If you **don’t** set an API key, the backend uses a **deterministic stub LLM** and a **built-in embedding** to keep everything fully local.
- If you set `OPENAI_API_KEY` or  `OPENROUTER_API_KEY`(or configure Ollama), the backend will use real models automatically.

## Project layout
```
ai-policy-helper/
├─ backend/
│  ├─ app/
│  │  ├─ main.py          # FastAPI app + endpoints
│  │  ├─ settings.py      # config/env
│  │  ├─ rag.py           # embeddings, vector store, retrieval, generation
│  │  ├─ models.py        # pydantic models
│  │  ├─ ingest.py        # doc loader & chunker
│  │  ├─ __init__.py
│  │  └─ tests/
│  │     ├─ conftest.py
│  │     └─ test_api.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/
│  ├─ app/
│  │  ├─ page.tsx         # chat UI
│  │  ├─ layout.tsx
│  │  └─ globals.css
│  ├─ components/
│  │  ├─ Chat.tsx
│  │  └─ AdminPanel.tsx
│  ├─ lib/api.ts
│  ├─ package.json
│  ├─ tsconfig.json
│  ├─ next.config.js
│  └─ Dockerfile
├─ data/                  # sample policy docs
├─ docker-compose.yml
├─ Makefile
└─ .env.example
```

## Tests
Run unit tests inside the backend container:
```bash
docker compose run --rm backend pytest -q
```
To run test locally, please refer to TESTS_README.md file for better clarity and steps