"""
Pytest configuration and shared fixtures for the testing suite.
Simplified for Windows compatibility.
"""
import pytest
import tempfile
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Add the src directory to the Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(backend_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import after path setup
try:
    from src.main import app
    from src.core.database import Base, get_db
    from src.models.agent import Agent
    from src.models.call import CallLog
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current Python path: {sys.path}")
    raise


# --- Test Database Setup ---
@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine using SQLite in memory."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False  # Set to True for SQL debugging
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create a test database session for each test."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Clean up all tables after each test
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with overridden database dependency."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# --- Mock Services (Fixed) ---
@pytest.fixture
def mock_llm_service():
    """Mock LLM service to avoid calling real Ollama."""
    mock_instance = Mock()
    mock_instance.get_response.return_value = "This is a test AI response."
    return mock_instance


@pytest.fixture
def mock_stt_service():
    """Mock STT service to avoid loading Whisper model."""
    mock_instance = Mock()
    mock_instance.transcribe.return_value = "This is test transcribed text."
    return mock_instance


@pytest.fixture
def mock_tts_service():
    """Mock TTS service to avoid loading TTS model."""
    mock_instance = Mock()
    mock_instance.synthesize.return_value = None
    return mock_instance


@pytest.fixture
def temp_audio_dir():
    """Create a temporary directory for audio files during testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


# --- Test Data Factories ---
@pytest.fixture
def sample_agent_data():
    """Sample agent data for testing."""
    return {
        "name": "Test Agent",
        "system_prompt": "You are a helpful test assistant.",
        "voice_id": "test_voice"
    }


@pytest.fixture
def sample_agent(test_db, sample_agent_data):
    """Create a sample agent in the test database."""
    agent = Agent(**sample_agent_data)
    test_db.add(agent)
    test_db.commit()
    test_db.refresh(agent)
    return agent
