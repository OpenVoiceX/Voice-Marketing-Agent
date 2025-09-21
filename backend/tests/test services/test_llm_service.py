"""
Tests for the LLM Service.
"""
import pytest
from unittest.mock import Mock, patch
from src.services.llm_service import LLMService


class TestLLMService:
    """Test cases for the LLM service."""

    @patch('src.services.llm_service.ollama.Client')
    @patch('src.core.config.settings')
    def test_llm_service_initialization(self, mock_settings, mock_ollama_client):
        """Test that LLM service initializes correctly."""
        # Mock the Ollama client
        mock_client_instance = Mock()
        mock_ollama_client.return_value = mock_client_instance
        mock_client_instance.show.return_value = {"model": "test_model"}
        
        # Create the service
        mock_settings.OLLAMA_HOST = "http://test:11434"
        mock_settings.LLM_MODEL_NAME = "test_model"
        
        service = LLMService()
        
        assert service.client == mock_client_instance
        assert service.model_name == "test_model"
        mock_client_instance.show.assert_called_once_with("test_model")

    @patch('src.services.llm_service.ollama.Client')
    @patch('src.core.config.settings')
    def test_get_response_success(self, mock_settings, mock_ollama_client):
        """Test successful response generation."""
        # Setup mocks
        mock_client_instance = Mock()
        mock_ollama_client.return_value = mock_client_instance
        mock_client_instance.show.return_value = {"model": "test_model"}
        mock_client_instance.chat.return_value = {
            "message": {"content": "Test AI response"}
        }
        
        # Create service and test
        mock_settings.OLLAMA_HOST = "http://test:11434"
        mock_settings.LLM_MODEL_NAME = "test_model"
        
        service = LLMService()
        messages = [{"role": "user", "content": "Hello"}]
        response = service.get_response(messages)
        
        assert response == "Test AI response"
        mock_client_instance.chat.assert_called_once_with(
            model="test_model",
            messages=messages
        )

    @patch('src.services.llm_service.ollama.Client')
    @patch('src.core.config.settings')
    def test_get_response_error_handling(self, mock_settings, mock_ollama_client):
        """Test error handling in response generation."""
        # Setup mocks to raise an exception
        mock_client_instance = Mock()
        mock_ollama_client.return_value = mock_client_instance
        mock_client_instance.show.return_value = {"model": "test_model"}
        mock_client_instance.chat.side_effect = Exception("Connection error")
        
        # Create service and test
        mock_settings.OLLAMA_HOST = "http://test:11434"
        mock_settings.LLM_MODEL_NAME = "test_model"
        
        service = LLMService()
        messages = [{"role": "user", "content": "Hello"}]
        response = service.get_response(messages)
        
        # Should return error message instead of crashing
        assert "I'm sorry, I'm having a little trouble thinking" in response