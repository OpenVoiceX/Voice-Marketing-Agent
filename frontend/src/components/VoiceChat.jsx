// frontend/src/components/VoiceChat.jsx
import { useState, useEffect, useRef } from 'react';
import '../assets/index.css';

const VoiceChat = ({ agentId, agentName, onClose }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [transcript, setTranscript] = useState([]);
  const [error, setError] = useState(null);
  
  const wsRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioContextRef = useRef(null);
  const recognitionRef = useRef(null);
  const synthRef = useRef(window.speechSynthesis);

  useEffect(() => {
    // Initialize Web Speech API for browser-based voice chat
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;

      recognitionRef.current.onresult = (event) => {
        const userText = event.results[0][0].transcript;
        handleUserSpeech(userText);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setError(`Speech recognition error: ${event.error}`);
        setIsRecording(false);
      };

      recognitionRef.current.onend = () => {
        setIsRecording(false);
      };
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      stopSpeaking();
    };
  }, []);

  const connectWebSocket = () => {
    const ws = new WebSocket(`ws://localhost:8000/api/v1/chat/voice/${agentId}`);
    
    ws.onopen = () => {
      setIsConnected(true);
      setError(null);
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.error) {
        setError(data.error);
        return;
      }

      if (data.type === 'agent_response') {
        addTranscript('agent', data.text);
        speakText(data.text);
      } else if (data.type === 'transcription') {
        addTranscript('user', data.text);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setError('Connection error. Please try again.');
      setIsConnected(false);
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    };

    wsRef.current = ws;
  };

  const handleUserSpeech = (text) => {
    addTranscript('user', text);
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'user_text',
        text: text
      }));
    }
  };

  const startRecording = () => {
    if (!isConnected) {
      connectWebSocket();
      // Wait for connection before recording
      setTimeout(() => {
        if (recognitionRef.current) {
          recognitionRef.current.start();
          setIsRecording(true);
        }
      }, 500);
    } else {
      if (recognitionRef.current) {
        recognitionRef.current.start();
        setIsRecording(true);
      }
    }
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsRecording(false);
    }
  };

  const speakText = (text) => {
    stopSpeaking(); // Stop any ongoing speech
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    
    synthRef.current.speak(utterance);
  };

  const stopSpeaking = () => {
    if (synthRef.current.speaking) {
      synthRef.current.cancel();
      setIsSpeaking(false);
    }
  };

  const addTranscript = (role, text) => {
    setTranscript(prev => [...prev, {
      role,
      text,
      timestamp: new Date().toLocaleTimeString()
    }]);
  };

  const handleClose = () => {
    if (wsRef.current) {
      wsRef.current.close();
    }
    stopSpeaking();
    stopRecording();
    onClose();
  };

  return (
    <div className="chat-overlay">
      <div className="chat-container voice-chat">
        <div className="chat-header">
          <div>
            <h3>🎤 Voice Chat with {agentName}</h3>
            <div className={`voice-status ${isConnected ? 'connected' : 'disconnected'}`}>
              {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
            </div>
          </div>
          <button onClick={handleClose} className="chat-close-btn">✕</button>
        </div>

        {error && (
          <div style={{ 
            padding: '1rem 1.5rem', 
            backgroundColor: '#fef2f2', 
            color: '#991b1b',
            borderBottom: '1px solid #fecaca',
            fontSize: '0.875rem'
          }}>
            ⚠️ {error}
          </div>
        )}

        <div className="chat-messages">
          {transcript.length === 0 && (
            <div style={{ textAlign: 'center', padding: '3rem 2rem', color: 'var(--text-muted)' }}>
              <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎙️</div>
              <p style={{ fontWeight: 500, fontSize: '1rem', marginBottom: '0.5rem' }}>
                Click "Start Talking" to begin voice conversation
              </p>
              <p style={{ fontSize: '0.875rem' }}>Speak naturally and the AI will respond</p>
            </div>
          )}
          {transcript.map((entry, index) => (
            <div key={index} className={`chat-message ${entry.role}`}>
              <div className="message-content">
                {entry.text}
              </div>
              <span className="message-time">{entry.timestamp}</span>
            </div>
          ))}
          {isSpeaking && (
            <div style={{ padding: '1rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              🔊 {agentName} is speaking...
            </div>
          )}
        </div>

        <div className="voice-controls">
          {!isConnected ? (
            <button onClick={connectWebSocket} className="button">
              Connect
            </button>
          ) : (
            <>
              <button
                onClick={isRecording ? stopRecording : startRecording}
                className={`voice-record-btn ${isRecording ? 'recording' : ''}`}
                disabled={isSpeaking}
              >
                {isRecording ? '⏹' : '🎤'}
              </button>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                {isRecording ? 'Recording... Click to stop' : 'Click to start talking'}
              </p>
              {isSpeaking && (
                <button onClick={stopSpeaking} className="button danger" style={{ marginTop: '0.5rem' }}>
                  Stop Speaking
                </button>
              )}
            </>
          )}
        </div>

        <div style={{ 
          padding: '1rem 1.5rem', 
          backgroundColor: 'var(--background-color)', 
          borderTop: '1px solid var(--border-color)',
          fontSize: '0.8125rem',
          color: 'var(--text-muted)',
          textAlign: 'center'
        }}>
          💡 Tip: Click "Start Talking", speak your message, then click "Stop Recording"
        </div>
      </div>
    </div>
  );
};

export default VoiceChat;
