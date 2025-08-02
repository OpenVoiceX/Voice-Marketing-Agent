// frontend/src/pages/CampaignsPage.jsx
import React, { useEffect, useState } from 'react';
import useCampaignStore from '../store/campaignStore';
import CampaignList from '../components/CampaignList';
import CampaignForm from '../components/CampaignForm';
import Button from '../components/common/Button';
import './CampaignsPage.css'; // We'll create this CSS file for styling

const CampaignsPage = () => {
  const { campaigns, loading, error, fetchCampaigns } = useCampaignStore();
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchCampaigns();
  }, [fetchCampaigns]);

  // Debug: Log campaigns to see what IDs exist
  useEffect(() => {
    if (campaigns.length > 0) {
      console.log('Available campaigns:', campaigns.map(c => ({ id: c.id, name: c.name })));
    }
  }, [campaigns]);

  return (
    <div>
      <div className="page-header">
        <h1>Call Campaigns</h1>
        <Button onClick={() => setIsModalOpen(true)}>+ New Campaign</Button>
      </div>

      {loading && <p>Loading campaigns...</p>}
      {error && <p className="error-message">Error: {error}</p>}
      
      {!loading && !error && (
        <CampaignList campaigns={campaigns} />
      )}

      {isModalOpen && (
        <div className="modal-backdrop">
          <div className="modal-content card">
            <CampaignForm onFormSubmit={() => setIsModalOpen(false)} />
            <Button className="modal-close-button" onClick={() => setIsModalOpen(false)}>Close</Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default CampaignsPage;