// frontend/src/store/campaignStore.js
import { create } from 'zustand';
import * as campaignApi from '../services/campaignApi';

const useCampaignStore = create((set, get) => ({
  campaigns: [],
  currentCampaign: null,
  loading: false,
  error: null,

  fetchCampaigns: async () => {
    set({ loading: true, error: null });
    try {
      const response = await campaignApi.getCampaigns();
      set({ campaigns: response.data, loading: false });
    } catch (error) {
      console.error('Error fetching campaigns:', error);
      set({ error: error.message, loading: false });
    }
  },

  fetchCampaignDetails: async (id) => {
    console.log('Store: fetchCampaignDetails called with ID:', id);
    set({ loading: true, error: null });
    try {
      const response = await campaignApi.getCampaignById(id);
      console.log('Store: Campaign data received:', response.data);
      set({ currentCampaign: response.data, loading: false, error: null });
    } catch (error) {
      console.error('Store: Error fetching campaign by ID:', error);
      set({ error: error.message, loading: false, currentCampaign: null });
    }
  },

  createCampaign: async (campaignData) => {
    set({ loading: true, error: null });
    try {
      await campaignApi.createCampaign(campaignData);
      await get().fetchCampaigns();
      set({ loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  deleteCampaign: async (id) => {
    set({ loading: true, error: null });
    try {
      await campaignApi.deleteCampaign(id);
      await get().fetchCampaigns();
      set({ loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  startCampaign: async (id) => {
    set({ loading: true, error: null });
    try {
      await campaignApi.startCampaign(id);
      await get().fetchCampaigns();
      // Optional: refetch the current campaign if it's the one being updated
      if (get().currentCampaign?.id === id) {
        await get().fetchCampaignDetails(id);
      }
      set({ loading: false });
    } catch (error) {
      console.error('Error starting campaign:', error);
      set({ error: error.message, loading: false });
    }
  },

  stopCampaign: async (id) => {
    set({ loading: true, error: null });
    try {
      await campaignApi.stopCampaign(id);
      await get().fetchCampaigns();
      if (get().currentCampaign?.id === id) {
        await get().fetchCampaignDetails(id);
      }
      set({ loading: false });
    } catch (error) {
      console.error('Error stopping campaign:', error);
      set({ error: error.message, loading: false });
    }
  },
}));

export default useCampaignStore;
