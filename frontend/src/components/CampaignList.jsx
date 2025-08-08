// frontend/src/components/CampaignList.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useCampaignStore from '../store/campaignStore';
import ConfirmationModal from './common/ConfirmationModal';

const CampaignList = ({ campaigns }) => {
  const {
    deleteCampaign,
    startCampaign,    // ✅ New
    stopCampaign      // ✅ New
  } = useCampaignStore();

  const navigate = useNavigate();
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, campaignId: null, campaignName: '' });

  const handleDeleteClick = (campaignId, campaignName) => {
    setDeleteModal({ isOpen: true, campaignId, campaignName });
  };

  const handleDeleteConfirm = async () => {
    if (deleteModal.campaignId) {
      await deleteCampaign(deleteModal.campaignId);
      setDeleteModal({ isOpen: false, campaignId: null, campaignName: '' });
    }
  };

  const handleDeleteCancel = () => {
    setDeleteModal({ isOpen: false, campaignId: null, campaignName: '' });
  };

  const handleViewClick = (campaignId) => {
    console.log('View button clicked for campaign ID:', campaignId);
    navigate(`/campaigns/${campaignId}`);
  };

  const handleStartClick = async (campaignId) => {
    await startCampaign(campaignId);
  };

  const handleStopClick = async (campaignId) => {
    await stopCampaign(campaignId);
  };

  if (campaigns.length === 0) {
    return <div className="card"><p>No campaigns found. Click "+ New Campaign" to get started!</p></div>;
  }

  return (
    <>
      <div className="card">
        <table className="campaign-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Agent ID</th>
              <th>Status</th>
              <th>Contacts</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {campaigns.map(campaign => (
              <tr key={campaign.id}>
                <td>{campaign.name}</td>
                <td>{campaign.agent_id}</td>
                <td>
                  <span className={`status-badge status-${campaign.status.toLowerCase()}`}>
                    {campaign.status}
                  </span>
                </td>
                <td>{campaign.contacts.length}</td>
                <td className="actions-cell space-x-1">
                  <button 
                    onClick={() => handleViewClick(campaign.id)}
                    className="action-link"
                    style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--primary-color)' }}
                  >
                    View
                  </button>
                  <button 
                    onClick={() => handleStartClick(campaign.id)}
                    className="action-link"
                    disabled={campaign.status === 'running'}
                  >
                    Start
                  </button>
                  <button 
                    onClick={() => handleStopClick(campaign.id)}
                    className="action-link"
                    disabled={campaign.status === 'stopped'}
                  >
                    Stop
                  </button>
                  <button 
                    onClick={() => handleDeleteClick(campaign.id, campaign.name)}
                    className="action-link delete-link"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <ConfirmationModal
        isOpen={deleteModal.isOpen}
        onClose={handleDeleteCancel}
        onConfirm={handleDeleteConfirm}
        title="Delete Campaign"
        message={`Are you sure you want to delete the campaign "${deleteModal.campaignName}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
        confirmButtonClass="danger"
      />
    </>
  );
};

export default CampaignList;
