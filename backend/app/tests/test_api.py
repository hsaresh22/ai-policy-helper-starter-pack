import json
import os
from unittest.mock import patch, MagicMock


def test_health(client):
    """Health endpoint should return ok status"""
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@patch('app.main.load_documents')
def test_ingest_and_ask(mock_load_docs, client):
    """Should ingest documents then ask questions"""
    # Mock document loading to return dummy docs
    mock_load_docs.return_value = [
        {"title": "Warranty_Policy.md", "section": "Coverage", "text": "Warranty covers defects for 1 year"},
        {"title": "Returns_Policy.md", "section": "Timeline", "text": "Returns accepted within 30 days"}
    ]
    
    r = client.post("/api/ingest")
    assert r.status_code == 200
    
    # Ask a deterministic question
    r2 = client.post("/api/ask", json={"query":"What is the refund window?"})
    assert r2.status_code == 200
    data = r2.json()
    assert "citations" in data
    assert "answer" in data and isinstance(data["answer"], str)


@patch('app.main.load_documents')
def test_ask_stream_returns_sse(mock_load_docs, client):
    """Stream endpoint should return SSE format"""
    mock_load_docs.return_value = [
        {"title": "Warranty_Policy.md", "section": "Coverage", "text": "Warranty covers defects for 1 year"}
    ]
    
    # First ingest
    client.post("/api/ingest")
    
    # Then ask with streaming
    r = client.post("/api/ask-stream", json={"query": "What is the warranty?"})
    assert r.status_code == 200
    assert "text/event-stream" in r.headers.get("content-type", "")
    
    # Should contain SSE data
    text = r.text
    assert "data:" in text
    assert "[DONE]" in text


@patch('app.main.load_documents')
def test_ask_stream_has_metadata(mock_load_docs, client):
    """Stream should include metadata with citations"""
    mock_load_docs.return_value = [
        {"title": "Policy.md", "section": "Main", "text": "Sample policy text"}
    ]
    
    client.post("/api/ingest")
    
    r = client.post("/api/ask-stream", json={"query": "test query"})
    text = r.text
    
    # Find and validate metadata event
    for line in text.split('\n'):
        if line.startswith('data: ') and 'metadata' in line:
            data = json.loads(line[6:])
            assert data.get("type") == "metadata"
            assert "citations" in data["data"]
            return
    
    assert False, "No metadata event found in stream"


def test_metrics_endpoint(client):
    """Metrics endpoint should return latency data"""
    r = client.get("/api/metrics")
    assert r.status_code == 200
    data = r.json()
    assert "avg_retrieval_latency_ms" in data
    assert "avg_generation_latency_ms" in data
