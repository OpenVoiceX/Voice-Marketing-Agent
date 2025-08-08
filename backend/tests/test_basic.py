"""
Basic tests to verify the testing setup works.
"""
import pytest


class TestBasicSetup:
    """Basic tests to verify everything is working."""

    def test_basic_math(self):
        """Test that basic Python works."""
        assert 1 + 1 == 2

    def test_imports(self):
        """Test that we can import our modules."""
        from src.models.agent import Agent
        from src.services.llm_service import LLMService
        assert Agent is not None
        assert LLMService is not None

    def test_database_fixture(self, test_db):
        """Test that database fixture works."""
        from src.models.agent import Agent
        
        # Create a test agent
        agent = Agent(
            name="Test Agent",
            system_prompt="Test prompt",
            voice_id="test_voice"
        )
        test_db.add(agent)
        test_db.commit()
        test_db.refresh(agent)
        
        assert agent.id is not None
        assert agent.name == "Test Agent"

    def test_api_client(self, client):
        """Test that the API client works."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"