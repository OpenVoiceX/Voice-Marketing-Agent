"""
Tests for the Agents API endpoints.
"""
import pytest
from src.models.agent import Agent


class TestAgentsAPI:
    """Test cases for the /api/v1/agents endpoints."""

    def test_create_agent_success(self, client):
        """Test successful agent creation."""
        agent_data = {
            "name": "API Test Agent",
            "system_prompt": "You are an API test assistant.",
            "voice_id": "api_test_voice"
        }
        
        response = client.post("/api/v1/agents/", json=agent_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == agent_data["name"]
        assert data["system_prompt"] == agent_data["system_prompt"]
        assert data["voice_id"] == agent_data["voice_id"]
        assert "id" in data

    def test_create_agent_missing_fields(self, client):
        """Test agent creation with missing required fields."""
        incomplete_data = {
            "name": "Incomplete Agent"
            # Missing system_prompt
        }
        
        response = client.post("/api/v1/agents/", json=incomplete_data)
        
        assert response.status_code == 422  # Validation error

    def test_get_agent_success(self, client, sample_agent):
        """Test retrieving a specific agent."""
        response = client.get(f"/api/v1/agents/{sample_agent.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_agent.id
        assert data["name"] == sample_agent.name

    def test_get_agent_not_found(self, client):
        """Test retrieving a non-existent agent."""
        response = client.get("/api/v1/agents/99999")
        
        assert response.status_code == 404
        assert "Agent not found" in response.json()["detail"]

    def test_get_agents_list(self, client, test_db):
        """Test retrieving the list of all agents."""
        # Create multiple test agents
        agents_data = [
            {"name": "Agent 1", "system_prompt": "Prompt 1", "voice_id": "voice1"},
            {"name": "Agent 2", "system_prompt": "Prompt 2", "voice_id": "voice2"},
        ]
        
        for agent_data in agents_data:
            agent = Agent(**agent_data)
            test_db.add(agent)
        test_db.commit()
        
        response = client.get("/api/v1/agents/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] in ["Agent 1", "Agent 2"]

    def test_get_agents_empty_list(self, client):
        """Test retrieving agents when none exist."""
        response = client.get("/api/v1/agents/")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
