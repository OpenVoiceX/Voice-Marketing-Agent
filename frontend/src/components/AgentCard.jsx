// frontend/src/components/AgentCard.jsx
import React, { useState } from 'react';
import { originateCall } from '../services/callApi';
import Button from './common/Button';
import Input from './common/Input';

const AgentCard = ({ agent }) => {
  const [toNumber, setToNumber] = useState('');
  const [status, setStatus] = useState({ message: '', type: '' });
  const [loading, setLoading] = useState(false);

  const handleCall = async () => {
    if (!toNumber) {
      setStatus({ message: 'Please enter a phone number.', type: 'error' });
      return;
    }
    setLoading(true);
    setStatus({ message: '', type: '' });

    try {
      const response = await originateCall(toNumber, agent.id);
      setStatus({ message: `Call initiated! SID: ${response.data.call_sid}`, type: 'success' });
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'An unknown error occurred.';
      setStatus({ message: `Error: ${errorMessage}`, type: 'error' });
      console.error("Call failed:", error.response || error);
    } finally {
      setLoading(false);
    }
  };

  // Function to get status badge styling and text
  const getStatusDisplay = (callStatus) => {
    // Handle both "calling" and "in_progress" as the same status since your backend uses "calling"
    const normalizedStatus = callStatus === 'calling' ? 'calling' : callStatus;
    
    const statusConfig = {
      idle: { 
        bg: '#6c757d', 
        color: 'white', 
        text: 'Idle', 
        icon: '💤' 
      },
      calling: { 
        bg: '#ffc107', 
        color: '#212529', 
        text: 'Calling...', 
        icon: '📞' 
      },
      completed: { 
        bg: '#28a745', 
        color: 'white', 
        text: 'Last Call: Completed', 
        icon: '✅' 
      },
      failed: { 
        bg: '#dc3545', 
        color: 'white', 
        text: 'Last Call: Failed', 
        icon: '❌' 
      }
    };

    const config = statusConfig[normalizedStatus] || statusConfig.idle;
    
    return (
      <span 
        style={{
          backgroundColor: config.bg,
          color: config.color,
          padding: '0.25rem 0.75rem',
          borderRadius: '20px',
          fontSize: '0.875rem',
          fontWeight: '500',
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.25rem'
        }}
      >
        <span>{config.icon}</span>
        <span>{config.text}</span>
      </span>
    );
  };

  // Determine if the agent is busy (calling)
  const isAgentBusy = agent.last_call_status === 'calling';

  return (
    <div className="card" style={{ marginBottom: '1rem' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'flex-start', 
        marginBottom: '1rem' 
      }}>
        <div>
          <h3 style={{ margin: '0 0 0.5rem 0' }}>{agent.name}</h3>
          <p style={{ margin: '0', color: '#666' }}>
            <strong>Agent ID:</strong> {agent.id}
          </p>
        </div>
        <div>
          {getStatusDisplay(agent.last_call_status)}
        </div>
      </div>
      
      <div style={{ margin: '1rem 0' }}>
        <Input
          label="Phone Number to Call"
          name={`toNumber-${agent.id}`}
          value={toNumber}
          onChange={(e) => setToNumber(e.target.value)}
          placeholder="+15551234567"
          disabled={isAgentBusy}
        />
      </div>
      
      <Button 
        onClick={handleCall} 
        disabled={loading || isAgentBusy}
      >
        {loading ? 'Calling...' : 
         isAgentBusy ? 'Agent Busy - Currently on Call' : 
         'Call with this Agent'}
      </Button>
      
      {status.message && (
        <p style={{ color: status.type === 'error' ? 'red' : 'green', marginTop: '1rem' }}>
          {status.message}
        </p>
      )}
    </div>
  );
};

export default AgentCard;