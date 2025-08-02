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
      set({ error: error.message, loading: false });
    }
  },

  fetchCampaignById: async (id) => {
    set({ loading: true, error: null, currentCampaign: null });
    try {
      const response = await campaignApi.getCampaignById(id);
      set({ currentCampaign: response.data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  createCampaign: async (campaignData) => {
    set({ loading: true, error: null });
    try {
      await campaignApi.createCampaign(campaignData);
      // After creating, refetch the list to show the new campaign
      await get().fetchCampaigns();
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  // --- NEW: Delete Campaign Action ---
  deleteCampaign: async (id) => {
    set({ loading: true, error: null });
    try {
      await campaignApi.deleteCampaign(id);
      // After deleting, refetch the list to update the UI
      await get().fetchCampaigns();
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
  // ----------------------------------
}));

export default useCampaignStore;