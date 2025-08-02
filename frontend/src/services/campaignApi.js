// frontend/src/services/campaignApi.js
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

// Debug: Log the API URL being used to ensure it's correct
console.log('API Base URL:', API_URL);

const apiClient = axios.create({
  baseURL: API_URL,
});

// Add a request interceptor for powerful debugging
// This will log every outgoing request to the browser console
apiClient.interceptors.request.use(
  (config) => {
    console.log('Making API request:', config.method?.toUpperCase(), config.url, config.data || '');
    return config;
  },
  (error) => {
    console.error('API request error:', error);
    return Promise.reject(error);
  }
);

// Add a response interceptor for powerful debugging
// This will log every incoming response or error to the browser console
apiClient.interceptors.response.use(
  (response) => {
    console.log('API response received:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API response error:', error.response?.status, error.response?.data, error.config?.url);
    return Promise.reject(error);
  }
);

// --- Campaign Endpoints ---
export const getCampaigns = () => apiClient.get('/campaigns/');
export const createCampaign = (campaignData) => apiClient.post('/campaigns/', campaignData);
export const getCampaignById = (id) => apiClient.get(`/campaigns/${id}`);
export const deleteCampaign = (id) => apiClient.delete(`/campaigns/${id}`);
export const startCampaign = (id) => apiClient.post(`/campaigns/${id}/start`);
export const stopCampaign = (id) => apiClient.post(`/campaigns/${id}/stop`);

// --- Contact Endpoints ---
export const addContactsToCampaign = (campaignId, file) => {
  const formData = new FormData();
  formData.append('file', file);

  return apiClient.post(`/campaigns/${campaignId}/contacts`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};