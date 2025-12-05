import pytest
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Add parent directory to path so 'app' can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)
