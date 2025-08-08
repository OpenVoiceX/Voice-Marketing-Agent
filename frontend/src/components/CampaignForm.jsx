// frontend/src/components/CampaignForm.jsx
import React, { useState, useEffect } from 'react';
import useCampaignStore from '../store/campaignStore';
import useAgentStore from '../store/agentStore';
import Button from './common/Button';
import Input from './common/Input';

const CampaignForm = ({ onFormSubmit }) => {
  const [name, setName] = useState('');
  const [agentId, setAgentId] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const createCampaign = useCampaignStore((state) => state.createCampaign);
  const { agents, fetchAgents } = useAgentStore();

  useEffect(() => {
    fetchAgents();
  }, [fetchAgents]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!name || !agentId) {
      setError('Please fill in all fields.');
      return;
    }

    setSubmitting(true);
    try {
      await createCampaign({ name, agent_id: parseInt(agentId) });
      setName('');
      setAgentId('');
      onFormSubmit(); // Close modal or reset UI
    } catch (err) {
      setError('Failed to create campaign. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create New Campaign</h2>

      {error && <p className="text-red-500 mb-2">{error}</p>}

      <Input
        label="Campaign Name"
        name="name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />

      <div className="form-group mb-4">
        <label htmlFor="agent_id">Select Agent</label>
        <select
          id="agent_id"
          name="agent_id"
          value={agentId}
          onChange={(e) => setAgentId(e.target.value)}
          required
          className="input"
        >
          <option value="" disabled>-- Choose an agent --</option>
          {agents.length === 0 ? (
            <option disabled>No agents available</option>
          ) : (
            agents.map(agent => (
              <option key={agent.id} value={agent.id}>
                {agent.name} (ID: {agent.id})
              </option>
            ))
          )}
        </select>
      </div>

      <Button type="submit" disabled={submitting}>
        {submitting ? 'Creating...' : 'Create Campaign'}
      </Button>
    </form>
  );
};

export default CampaignForm;
