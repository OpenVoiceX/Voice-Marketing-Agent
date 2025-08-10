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
      // --- THIS IS THE CRITICAL PART ---
      // We are sending the correct keys: 'to_number' and 'agent_id'
      const response = await originateCall(toNumber, agent.id);
      // ---------------------------------

      setStatus({ message: `Call initiated! SID: ${response.data.call_sid}`, type: 'success' });
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'An unknown error occurred.';
      setStatus({ message: `Error: ${errorMessage}`, type: 'error' });
      console.error("Call failed:", error.response || error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ marginBottom: '1rem' }}>
      <h3>{agent.name}</h3>
      <p><strong>Agent ID:</strong> {agent.id}</p>
      <div style={{ margin: '1rem 0' }}>
        <Input
          label="Phone Number to Call"
          name={`toNumber-${agent.id}`}
          value={toNumber}
          onChange={(e) => setToNumber(e.target.value)}
          placeholder="+15551234567"
        />
      </div>
      <Button onClick={handleCall} disabled={loading}>
        {loading ? 'Calling...' : 'Call with this Agent'}
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