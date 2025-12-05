"""
Essential unit tests for RAG components
"""
import pytest
import numpy as np
from app.rag import LocalEmbedder, InMemoryStore, StubLLM


class TestLocalEmbedder:
    """Tests for deterministic local embeddings"""
    
    def test_embed_returns_correct_dimension(self):
        """Embedding output should match specified dimension"""
        embedder = LocalEmbedder(dim=384)
        emb = embedder.embed("test text")
        assert emb.shape == (384,)
        assert emb.dtype == np.float32
    
    def test_embed_deterministic(self):
        """Same input should produce identical embeddings"""
        embedder = LocalEmbedder(dim=384)
        text = "What is the warranty policy?"
        
        emb1 = embedder.embed(text)
        emb2 = embedder.embed(text)
        
        assert np.allclose(emb1, emb2), "Embeddings should be deterministic"
    
    def test_embed_l2_normalized(self):
        """Embeddings should be L2-normalized"""
        embedder = LocalEmbedder(dim=384)
        emb = embedder.embed("Test document")
        
        norm = np.linalg.norm(emb)
        assert np.isclose(norm, 1.0, atol=1e-6), "Embedding should be L2-normalized"


class TestInMemoryStore:
    """Tests for in-memory vector store"""
    
    def test_initialization(self):
        """Store should initialize with correct dimension"""
        store = InMemoryStore(dim=384)
        assert store.dim == 384
        assert len(store.vecs) == 0
    
    def test_upsert_single_vector(self):
        """Should add single vector to store"""
        store = InMemoryStore(dim=384)
        vec = np.random.randn(384).astype("float32")
        meta = {"title": "Policy", "hash": "abc123"}
        
        store.upsert([vec], [meta])
        
        assert len(store.vecs) == 1
        assert store.meta[0]["title"] == "Policy"
    
    def test_search_returns_results(self):
        """Search should return results"""
        embedder = LocalEmbedder(dim=384)
        store = InMemoryStore(dim=384)
        
        # Add document
        vec = embedder.embed("warranty policy")
        store.upsert([vec], [{"title": "Warranty", "text": "Coverage"}])
        
        # Search with similar query
        query_vec = embedder.embed("warranty")
        results = store.search(query_vec, k=1)
        
        assert len(results) == 1
        assert results[0][1]["title"] == "Warranty"


class TestStubLLM:
    """Tests for deterministic stub LLM"""
    
    def test_generate_response(self):
        """Stub LLM should generate a response"""
        llm = StubLLM()
        contexts = [{"title": "Policy", "section": "Terms", "text": "Coverage"}]
        
        response = llm.generate("What is covered?", contexts)
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert "Policy" in response
