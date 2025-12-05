# Running Tests

## Backend Tests

### Install Dependencies
```bash
cd backend
pip install pytest pytest-mock pytest-asyncio
```

### Run Tests
```bash
# All backend tests
pytest

# Specific test file
pytest app/tests/test_api.py -v

# Specific test
pytest app/tests/test_rag.py::TestLocalEmbedder::test_embed_deterministic -v

# With coverage
pytest --cov=app --cov-report=html
```

## Frontend Tests

### Install Dependencies
```bash
cd frontend
npm install
```

Jest and testing libraries are already in `package.json` devDependencies.

### Run Tests
```bash
# All frontend tests
npm test

# Watch mode
npm test -- --watch

# With coverage
npm test -- --coverage
```

## Test Files

**Backend:**
- `backend/app/tests/test_rag.py` - Unit tests for embeddings, vector stores, LLM
- `backend/app/tests/test_api.py` - Integration tests for FastAPI endpoints

**Frontend:**
- `frontend/__tests__/chat.test.ts` - Component and API client tests

## What's Tested

### Backend
- ✅ Embeddings (determinism, normalization, L2)
- ✅ Vector store operations (add, search)
- ✅ LLM response generation
- ✅ API endpoints (health, ingest, ask, ask-stream, metrics)
- ✅ SSE streaming format
- ✅ Metadata in streams

### Frontend
- ✅ Chat component rendering
- ✅ Message streaming
- ✅ Citations display
- ✅ Auto-scroll behavior
- ✅ SSE parsing
- ✅ UTF-8 handling
- ✅ Error handling
