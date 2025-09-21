"""
Tests for the Appointment Setter Agent logic.
"""
import pytest
from unittest.mock import Mock
from src.agents.appointment_setter.logic import AppointmentSetterAgent


class TestAppointmentSetterAgent:
    """Test cases for the Appointment Setter Agent."""

    def test_agent_initialization(self):
        """Test agent initialization with system prompt."""
        mock_llm_service = Mock()
        system_prompt = "You are a test agent."
        
        agent = AppointmentSetterAgent(mock_llm_service, system_prompt)
        
        assert agent.llm_service == mock_llm_service
        assert agent.system_prompt == system_prompt

    def test_get_initial_greeting(self):
        """Test the initial greeting generation."""
        mock_llm_service = Mock()
        agent = AppointmentSetterAgent(mock_llm_service, "Test prompt")
        
        greeting = agent.get_initial_greeting()
        
        assert isinstance(greeting, str)
        assert len(greeting) > 0
        assert "AI assistant" in greeting

    def test_process_response(self):
        """Test processing user response."""
        mock_llm_service = Mock()
        mock_llm_service.get_response.return_value = "Test AI response"
        
        agent = AppointmentSetterAgent(mock_llm_service, "You are a test agent.")
        
        response = agent.process_response("Hello", [])
        
        assert response == "Test AI response"
        mock_llm_service.get_response.assert_called_once()
        
        # Verify the messages structure
        call_args = mock_llm_service.get_response.call_args[0][0]
        assert call_args[0]["role"] == "system"
        assert call_args[0]["content"] == "You are a test agent."
        assert call_args[1]["role"] == "user"
        assert call_args[1]["content"] == "Hello"

    def test_process_response_with_history(self):
        """Test processing response with conversation history."""
        mock_llm_service = Mock()
        mock_llm_service.get_response.return_value = "Response with history"
        
        agent = AppointmentSetterAgent(mock_llm_service, "Test prompt")
        
        history = [
            {"role": "user", "content": "Previous user message"},
            {"role": "assistant", "content": "Previous assistant message"}
        ]
        
        response = agent.process_response("New message", history)
        
        assert response == "Response with history"
        
        # Verify history is included in the messages
        call_args = mock_llm_service.get_response.call_args[0][0]
        assert len(call_args) == 4  # system + history + new user message
        assert call_args[1] == history[0]
        assert call_args[2] == history[1]