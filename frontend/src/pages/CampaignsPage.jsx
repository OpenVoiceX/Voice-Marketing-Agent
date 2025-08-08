// frontend/src/pages/CampaignsPage.jsx
import React, { useEffect, useState, useCallback } from 'react';
import useCampaignStore from '../store/campaignStore';
import CampaignList from '../components/CampaignList';
import CampaignForm from '../components/CampaignForm';
import Button from '../components/common/Button';
import './CampaignsPage.css';

const CampaignsPage = () => {
  const { campaigns, loading, error, fetchCampaigns } = useCampaignStore();
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchCampaigns();
  }, [fetchCampaigns]);

  // Debug log for development
  useEffect(() => {
    if (campaigns.length > 0) {
      console.log('Available campaigns:', campaigns.map(c => ({ id: c.id, name: c.name })));
    }
  }, [campaigns]);

  // Escape key to close modal
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') setIsModalOpen(false);
    };
    if (isModalOpen) {
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isModalOpen]);

  // Background click closes modal
  const handleBackdropClick = useCallback((e) => {
    if (e.target.classList.contains('modal-backdrop')) {
      setIsModalOpen(false);
    }
  }, []);

  return (
    <div className="campaigns-page">
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
        <div className="modal-backdrop" onClick={handleBackdropClick}>
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
