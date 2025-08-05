"""
Tests for the Agents API endpoints.
"""
import pytest


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

    def test_get_agents_empty_list(self, client):
        """Test retrieving agents when none exist."""
        response = client.get("/api/v1/agents/")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_agent_not_found(self, client):
        """Test retrieving a non-existent agent."""
        response = client.get("/api/v1/agents/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "Agent not found" in data["detail"]
