// frontend/src/services/agentApi.js
import axios from 'axios';

// The base URL should point to your backend API.
// In development, this is empty so we use the proxy. In production, Nginx will handle it.
const API_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const apiClient = axios.create({
  baseURL: API_URL,
});

export const getAgents = () => {
  return apiClient.get('/agents/');
};

export const getAgentById = (agentId) => {
  return apiClient.get(`/agents/${agentId}`);
};

export const createAgent = (agentData) => {
  return apiClient.post('/agents/', agentData);
};

export const getAgentOptions = async () => {
  const response = await apiClient.get('/agents/options/config');
  return response.data;
};

// --- ADD THIS NEW FUNCTION ---
export const originateCall = (agentId, phoneNumber) => {
  return apiClient.post('/calls/originate', {
    agent_id: agentId,
    phone_number: phoneNumber,
  });
};