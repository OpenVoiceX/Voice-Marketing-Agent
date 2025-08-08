// frontend/src/pages/AgentsPage.jsx
import React, { useEffect } from 'react';
import AgentForm from '../components/AgentForm';
import useAgentStore from '../store/agentStore';
import AgentCard from '../components/AgentCard'; // <-- IMPORT THE NEW COMPONENT
import SkeletonCard from '../components/common/SkeletonCard';

const AgentsPage = () => {
  const { agents, loading, error, fetchAgents } = useAgentStore();

  useEffect(() => {
    // This is called when the component first loads
    fetchAgents();
  }, [fetchAgents]);

  return (
    <div>
      <div className="page-header">
        <h1>Voice Agents</h1>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
        <div>
          <h2>Existing Agents</h2>
          {loading && (
            <>
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
            </>
          )}

          {error && <p style={{ color: 'red' }}>Error: {error}</p>}
          
          {/* --- USE THE NEW AGENT CARD COMPONENT --- */}
          {!loading && agents.length > 0 && (
            <div>
              {agents.map((agent) => (
                <AgentCard key={agent.id} agent={agent} />
              ))}
            </div>
          )}
          {/* ----------------------------------------- */}

          {!loading && agents.length === 0 && <p>No agents created yet. Use the form on the right to create one!</p>}
        </div>
        <div>
          <AgentForm onFormSubmit={fetchAgents} />
        </div>
      </div>
    </div>
  );
};

export default AgentsPage;