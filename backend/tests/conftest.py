"""
Pytest configuration and shared fixtures for the testing suite.
"""
import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from src.main import app
from src.core.database import Base, get_db
from src.core.config import settings
from src.models.agent import Agent
from src.models.call import CallLog


# --- Test Database Setup ---
@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine using SQLite in memory."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
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
        for table in reversed(Base.metadata.sorted_tables):
            test_engine.execute(table.delete())


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


# --- Mock Services ---
@pytest.fixture
def mock_llm_service():
    """Mock LLM service to avoid calling real Ollama."""
    with patch('src.services.llm_service.LLMService') as mock:
        mock_instance = Mock()
        mock_instance.get_response.return_value = "This is a test AI response."
        mock.return_value = mock_instance
        yield mock_instance


# One more fix needed - update the STT service import to match actual file
@pytest.fixture
def mock_stt_service():
    """Mock STT service to avoid loading Whisper model."""
    with patch('src.services.stt_service.STTService') as mock:
        mock_instance = Mock()
        mock_instance.transcribe.return_value = "This is test transcribed text."
        mock.return_value = mock_instance
        yield mock_instance


# Fix the config reference in the STT service file
@pytest.fixture
def mock_stt_service_fixed():
    """Mock STT service with correct config references."""
    with patch('src.services.stt_service.WhisperModel') as mock_whisper:
        mock_instance = Mock()
        mock_instance.transcribe.return_value = (
            [Mock(text="This is test transcribed text.")], 
            Mock(language="en", language_probability=0.9)
        )
        mock_whisper.return_value = mock_instance
        
        with patch('src.services.stt_service.settings') as mock_settings:
            mock_settings.WHISPER_MODEL_SIZE = "base"
            yield mock_instance


@pytest.fixture
def mock_tts_service():
    """Mock TTS service to avoid loading Coqui TTS."""
    with patch('src.services.tts_service.TTSService') as mock:
        mock_instance = Mock()
        mock_instance.synthesize.return_value = None  # Just pretend it worked
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def temp_audio_dir():
    """Create a temporary directory for audio files during testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Override the audio directory setting
        original_audio_dir = settings.AUDIO_DIR
        settings.AUDIO_DIR = temp_dir
        yield temp_dir
        settings.AUDIO_DIR = original_audio_dir


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
