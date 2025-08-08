// frontend/src/services/campaignApi.js
import axios from 'axios';

const API_URL = '/api/v1'; // Update this if needed (e.g., from environment)
console.log('API Base URL:', API_URL);

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

// Request Interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response Interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    if (error.response) {
      console.error('API Response Error:', error.response.status, error.response.data?.message || error.message);
    } else {
      console.error('API Response Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// --- Campaign Endpoints ---
export const getCampaigns = () => apiClient.get('/campaigns/');
export const createCampaign = (campaignData) => apiClient.post('/campaigns/', campaignData);
export const getCampaignById = (id) => apiClient.get(`/campaigns/${id}/`);
export const getCampaignDetails = getCampaignById;

export const getCampaignStatus = (id) => apiClient.get(`/campaigns/${id}/status/`);
export const deleteCampaign = (id) => apiClient.delete(`/campaigns/${id}/`);
export const startCampaign = (id) => apiClient.post(`/campaigns/${id}/start/`);
export const stopCampaign = (id) => apiClient.post(`/campaigns/${id}/stop/`);

// --- Contact Endpoints ---
export const addContactsToCampaign = (campaignId, file) => {
  const formData = new FormData();
  formData.append('file', file);

  return apiClient.post(`/campaigns/${campaignId}/contacts/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Optional: If needed
// export const getCampaignContacts = (id) => apiClient.get(`/campaigns/${id}/contacts/`);
