// frontend/src/components/CampaignList.jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import useCampaignStore from '../store/campaignStore';
import ConfirmationModal from './common/ConfirmationModal';

const CampaignList = ({ campaigns }) => {
  const { deleteCampaign } = useCampaignStore();
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
                <td className="actions-cell">
                  <Link to={`/campaigns/${campaign.id}`} className="action-link">View</Link>
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