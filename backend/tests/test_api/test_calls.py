"""
Tests for the Calls API endpoints.
"""
import pytest
from unittest.mock import patch, Mock
import tempfile
import os


class TestCallsAPI:
    """Test cases for the /api/v1/calls endpoints."""

    def test_webhook_initial_call(self, client, sample_agent, mock_llm_service, mock_tts_service, temp_audio_dir):
        """Test the webhook endpoint for initial call (no SpeechResult)."""
        with patch('src.api.routes.calls.AppointmentSetterAgent') as mock_agent_class:
            # Setup mock agent
            mock_agent_instance = Mock()
            mock_agent_instance.get_initial_greeting.return_value = "Hello, this is a test greeting."
            mock_agent_class.return_value = mock_agent_instance
            
            # Make the request
            response = client.post(
                "/api/v1/calls/webhook",
                data={"agent_id": sample_agent.id}
            )
            
            assert response.status_code == 200
            assert response.headers["content-type"] == "application/xml"
            
            # Verify XML contains expected TwiML elements
            xml_content = response.content.decode()
            assert "<Response>" in xml_content
            assert "<Play>" in xml_content
            assert "<Gather>" in xml_content

    def test_webhook_with_speech_result(self, client, sample_agent, mock_llm_service, mock_tts_service, temp_audio_dir):
        """Test the webhook endpoint with user speech input."""
        with patch('src.api.routes.calls.AppointmentSetterAgent') as mock_agent_class:
            # Setup mock agent
            mock_agent_instance = Mock()
            mock_agent_instance.process_response.return_value = "Thank you for your response."
            mock_agent_class.return_value = mock_agent_instance
            
            # Make the request with speech result
            response = client.post(
                "/api/v1/calls/webhook",
                data={
                    "agent_id": sample_agent.id,
                    "SpeechResult": "Yes, I'm interested"
                }
            )
            
            assert response.status_code == 200
            assert response.headers["content-type"] == "application/xml"
            
            # Verify agent was called with the speech result
            mock_agent_instance.process_response.assert_called_once_with(
                "Yes, I'm interested", 
                conversation_history=[]
            )

    def test_webhook_agent_not_found(self, client, mock_llm_service, mock_tts_service):
        """Test webhook with non-existent agent ID."""
        response = client.post(
            "/api/v1/calls/webhook",
            data={"agent_id": 99999}
        )
        
        assert response.status_code == 404
        assert "Agent with ID 99999 not found" in response.json()["detail"]

    @patch('src.api.routes.calls.Client')  # Mock Twilio Client
    @patch.dict(os.environ, {
        'TWILIO_ACCOUNT_SID': 'test_sid',
        'TWILIO_AUTH_TOKEN': 'test_token',
        'TWILIO_PHONE_NUMBER': '+15551234567',
        'PUBLIC_URL': 'http://test.example.com'
    })
    def test_originate_call_success(self, mock_twilio_client, client, sample_agent):
        """Test successful call origination."""
        # Setup mock Twilio client
        mock_client_instance = Mock()
        mock_call = Mock()
        mock_call.sid = "CA1234567890"
        mock_client_instance.calls.create.return_value = mock_call
        mock_twilio_client.return_value = mock_client_instance
        
        # Make the request
        response = client.post(
            "/api/v1/calls/originate",
            json={
                "phone_number": "+15559876543",
                "agent_id": sample_agent.id
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["call_sid"] == "CA1234567890"
        
        # Verify Twilio client was called correctly
        mock_client_instance.calls.create.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    def test_originate_call_missing_twilio_config(self, client, sample_agent):
        """Test call origination without Twilio configuration."""
        response = client.post(
            "/api/v1/calls/originate",
            json={
                "phone_number": "+15559876543",
                "agent_id": sample_agent.id
            }
        )
        
        assert response.status_code == 500
        assert "TWILIO environment variables are missing" in response.json()["detail"]
