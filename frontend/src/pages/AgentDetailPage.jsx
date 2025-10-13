// frontend/src/pages/AgentDetailPage.jsx
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import useAgentStore from '../store/agentStore';
import TextChat from '../components/TextChat';
import VoiceChat from '../components/VoiceChat';
import CallInitiationForm from '../components/CallInitiationForm';

const AgentDetailPage = () => {
  const { agentId } = useParams();
  const { currentAgent, fetchAgentById, loading, error } = useAgentStore();
  const [showTextChat, setShowTextChat] = useState(false);
  const [showVoiceChat, setShowVoiceChat] = useState(false);
  const [showCallForm, setShowCallForm] = useState(false);

  useEffect(() => {
    fetchAgentById(agentId);
  }, [agentId, fetchAgentById]);

  if (loading) return <p>Loading agent details...</p>;
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>;
  if (!currentAgent) return <p>Agent not found.</p>;

  return (
    <div>
      <div className="page-header">
        <h1>Agent: {currentAgent.name}</h1>
        <Link to="/agents">Back to Agents</Link>
      </div>

      {/* Action Buttons */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h3>💬 Interact with Agent</h3>
        <p style={{ marginBottom: '1rem', color: '#666' }}>
          Choose how you want to interact with {currentAgent.name}:
        </p>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <button
            onClick={() => setShowTextChat(true)}
            className="btn"
            style={{ background: '#4a90e2', color: 'white' }}
          >
            💬 Text Chat
          </button>
          <button
            onClick={() => setShowVoiceChat(true)}
            className="btn"
            style={{ background: '#6c63ff', color: 'white' }}
          >
            🎤 Voice Chat (Web)
          </button>
          <button
            onClick={() => setShowCallForm(true)}
            className="btn"
            style={{ background: '#28a745', color: 'white' }}
          >
            📞 Phone Call
          </button>
        </div>
      </div>

      {/* Agent Details */}
      <div className="card">
        <h3>Agent Configuration</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <p><strong>ID:</strong> {currentAgent.id}</p>
            <p><strong>Name:</strong> {currentAgent.name}</p>
          </div>
          <div>
            <p><strong>LLM Provider:</strong> {currentAgent.llm_provider || 'gemini'}</p>
            <p><strong>Model:</strong> {currentAgent.llm_model || 'gemini-1.5-flash'}</p>
          </div>
          <div>
            <p><strong>Voice ID:</strong> {currentAgent.tts_voice_id || currentAgent.voice_id}</p>
            <p><strong>STT Provider:</strong> {currentAgent.stt_provider || 'deepgram'}</p>
          </div>
        </div>
        <h3>System Prompt</h3>
        <pre style={{ whiteSpace: 'pre-wrap', backgroundColor: '#f0f0f0', padding: '1rem', borderRadius: '6px' }}>
          {currentAgent.system_prompt}
        </pre>
      </div>

      {/* Chat Modals */}
      {showTextChat && (
        <TextChat
          agentId={currentAgent.id}
          agentName={currentAgent.name}
          onClose={() => setShowTextChat(false)}
        />
      )}

      {showVoiceChat && (
        <VoiceChat
          agentId={currentAgent.id}
          agentName={currentAgent.name}
          onClose={() => setShowVoiceChat(false)}
        />
      )}

      {showCallForm && (
        <div className="chat-overlay">
          <div className="chat-container" style={{ maxHeight: '400px', height: 'auto' }}>
            <div className="chat-header">
              <h3>📞 Initiate Phone Call</h3>
              <button onClick={() => setShowCallForm(false)} className="chat-close-btn">✕</button>
            </div>
            <div style={{ padding: '1.5rem' }}>
              <CallInitiationForm agentId={currentAgent.id} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AgentDetailPage;