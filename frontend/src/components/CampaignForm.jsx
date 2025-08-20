// frontend/src/components/CampaignForm.jsx
import React, { useState, useEffect } from 'react';
import useCampaignStore from '../store/campaignStore';
import useAgentStore from '../store/agentStore';
import Button from './common/Button';
import Input from './common/Input';

const CampaignForm = ({ onFormSubmit }) => {
  const [name, setName] = useState('');
  const [agentId, setAgentId] = useState('');
  const createCampaign = useCampaignStore((state) => state.createCampaign);
  const { agents, fetchAgents } = useAgentStore();

  useEffect(() => {
    // Fetch agents to populate the dropdown
    fetchAgents();
  }, [fetchAgents]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name || !agentId) return;
    
    await createCampaign({ name, agent_id: parseInt(agentId) });
    onFormSubmit(); // Close the modal
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create New Campaign</h2>
      <Input
        label="Campaign Name"
        name="name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <div className="form-group">
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
          {agents.map(agent => (
            <option key={agent.id} value={agent.id}>{agent.name} (ID: {agent.id})</option>
          ))}
        </select>
      </div>
      <Button type="submit">Create Campaign</Button>
    </form>
  );
};

export default CampaignForm;