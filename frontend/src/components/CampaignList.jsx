// frontend/src/components/CampaignList.jsx
import React, { useState } from 'react';

const CampaignList = ({ campaigns, startCampaign, stopCampaign }) => {
  const [submittingId, setSubmittingId] = useState(null);

  const handleStartClick = async (campaignId) => {
    if (submittingId) return; // prevent multiple clicks
    setSubmittingId(campaignId);
    try {
      await startCampaign(campaignId);
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        'Failed to start campaign.';
      alert(msg); // Replace with toast if your project uses one
    } finally {
      setSubmittingId(null);
    }
  };

  const handleStopClick = async (campaignId) => {
    if (submittingId) return; // prevent multiple clicks
    setSubmittingId(campaignId);
    try {
      await stopCampaign(campaignId);
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        'Failed to stop campaign.';
      alert(msg); // Replace with toast if your project uses one
    } finally {
      setSubmittingId(null);
    }
  };

  return (
    <div className="campaign-list">
      {campaigns.map((campaign) => (
        <div key={campaign.id} className="campaign-item">
          <span>{campaign.name}</span>
          <button
            onClick={() => handleStartClick(campaign.id)}
            disabled={submittingId === campaign.id}
          >
            {submittingId === campaign.id ? 'Starting...' : 'Start'}
          </button>
          <button
            onClick={() => handleStopClick(campaign.id)}
            disabled={submittingId === campaign.id}
          >
            {submittingId === campaign.id ? 'Stopping...' : 'Stop'}
          </button>
        </div>
      ))}
    </div>
  );
};

export default CampaignList;
