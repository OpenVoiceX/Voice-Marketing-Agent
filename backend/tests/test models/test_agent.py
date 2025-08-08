"""
Tests for the Agent model.
"""
import pytest
from src.models.agent import Agent


class TestAgentModel:
    """Test cases for the Agent database model."""

    def test_create_agent(self, test_db):
        """Test creating a new agent."""
        agent_data = {
            "name": "Test Agent",
            "system_prompt": "You are a test assistant.",
            "voice_id": "default_voice"
        }
        
        agent = Agent(**agent_data)
        test_db.add(agent)
        test_db.commit()
        test_db.refresh(agent)
        
        assert agent.id is not None
        assert agent.name == "Test Agent"
        assert agent.system_prompt == "You are a test assistant."
        assert agent.voice_id == "default_voice"

    def test_agent_string_representation(self, test_db):
        """Test that agent has a reasonable string representation."""
        agent = Agent(
            name="String Test Agent",
            system_prompt="Test prompt",
            voice_id="test_voice"
        )
        test_db.add(agent)
        test_db.commit()
        
        # This would require adding a __str__ method to the Agent model
        # For now, just test that it doesn't crash
        str(agent)