// frontend/src/pages/CampaignDetailPage.jsx
import React, { useEffect, useState, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import useCampaignStore from '../store/campaignStore';
import { addContactsToCampaign, startCampaign, stopCampaign } from '../services/campaignApi';
import Button from '../components/common/Button';
import './CampaignDetailPage.css';

const CampaignDetailPage = () => {
  const { campaignId } = useParams();
  const { currentCampaign, loading, error, fetchCampaignById } = useCampaignStore();
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState({ message: '', type: '' });
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchCampaignById(campaignId);
  }, [campaignId, fetchCampaignById]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadStatus({ message: '', type: '' }); // Clear status on new file selection
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus({ message: 'Please select a CSV file first.', type: 'error' });
      return;
    }
    setUploadStatus({ message: 'Uploading...', type: 'info' });

    try {
      const response = await addContactsToCampaign(campaignId, file);
      setUploadStatus({ message: response.data.message, type: 'success' });
      // Refresh campaign data to show new contacts
      fetchCampaignById(campaignId);
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      setFile(null);
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      setUploadStatus({ message: `Upload failed: ${errorMessage}`, type: 'error' });
    }
  };
  
  const handleStart = async () => {
    await startCampaign(campaignId);
    fetchCampaignById(campaignId); // Refresh to show new status
  };

  const handleStop = async () => {
    await stopCampaign(campaignId);
    fetchCampaignById(campaignId); // Refresh
  };

  if (loading && !currentCampaign) return <p>Loading campaign details...</p>;
  if (error) return <p className="error-message">Error: {error}</p>;
  if (!currentCampaign) return <p>Campaign not found.</p>;

  return (
    <div>
      <Link to="/campaigns" className="back-link">← Back to Campaigns</Link>
      <div className="page-header">
        <h1>{currentCampaign.name}</h1>
        <div className="campaign-actions">
          <Button onClick={handleStop} className="secondary-button">Pause</Button>
          <Button onClick={handleStart}>Start Campaign</Button>
        </div>
      </div>

      <div className="campaign-stats card">
        <div><strong>Status:</strong> <span className={`status-badge status-${currentCampaign.status.toLowerCase()}`}>{currentCampaign.status}</span></div>
        <div><strong>Agent ID:</strong> {currentCampaign.agent_id}</div>
        <div><strong>Contacts:</strong> {currentCampaign.contacts.length}</div>
      </div>

      <div className="card">
        <h2>Manage Contacts</h2>
        <div className="upload-section">
          <p>Upload a CSV file with a 'phone_number' column to add contacts.</p>
          <input type="file" accept=".csv" onChange={handleFileChange} ref={fileInputRef} />
          <Button onClick={handleUpload} disabled={!file || loading}>Upload Contacts</Button>
        </div>
        {uploadStatus.message && (
          <p className={`status-message type-${uploadStatus.type}`}>
            {uploadStatus.message}
          </p>
        )}
        <h3>Contact List</h3>
        <table className="contact-table">
          <thead>
            <tr>
              <th>Phone Number</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {currentCampaign.contacts.length > 0 ? (
              currentCampaign.contacts.map(contact => (
                <tr key={contact.id}>
                  <td>{contact.phone_number}</td>
                  <td><span className={`status-badge status-${contact.status.toLowerCase()}`}>{contact.status}</span></td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="2">No contacts found for this campaign.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CampaignDetailPage;