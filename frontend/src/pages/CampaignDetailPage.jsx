// frontend/src/pages/CampaignDetailPage.jsx
import React, { useEffect, useState, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import useCampaignStore from '../store/campaignStore';
import { addContactsToCampaign, startCampaign, stopCampaign, getCampaignStatus } from '../services/campaignApi';
import Button from '../components/common/Button';
import './CampaignDetailPage.css';

const CampaignDetailPage = () => {
  const { campaignId } = useParams();
  const { currentCampaign, loading, error, fetchCampaignById } = useCampaignStore();
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState({ message: '', type: '' });
  const [isStarting, setIsStarting] = useState(false);
  const [campaignStatus, setCampaignStatus] = useState(null);
  const [currentlyCalling, setCurrentlyCalling] = useState(null);
  
  // Refs for managing intervals
  const statusIntervalRef = useRef(null);
  const campaignIntervalRef = useRef(null);

  // Load campaign data
  useEffect(() => {
    if (campaignId) {
      fetchCampaignById(campaignId);
    }
  }, [campaignId, fetchCampaignById]);

  // Real-time status updates
  useEffect(() => {
    const loadStatus = async () => {
      if (campaignId) {
        try {
          const response = await getCampaignStatus(campaignId);
          setCampaignStatus(response.data);
        } catch (error) {
          console.error('Failed to fetch campaign status:', error);
        }
      }
    };
    
    // Load status immediately
    loadStatus();
    
    // Set up polling for status updates (every 3 seconds)
    statusIntervalRef.current = setInterval(loadStatus, 3000);
    
    return () => {
      if (statusIntervalRef.current) {
        clearInterval(statusIntervalRef.current);
      }
    };
  }, [campaignId]);

  // Real-time campaign data updates (when campaign is running)
  useEffect(() => {
    const updateCampaignData = async () => {
      if (campaignId && currentCampaign?.status === 'running') {
        await fetchCampaignById(campaignId);
      }
    };

    // Update campaign data every 5 seconds when running
    if (currentCampaign?.status === 'running') {
      campaignIntervalRef.current = setInterval(updateCampaignData, 5000);
    }

    return () => {
      if (campaignIntervalRef.current) {
        clearInterval(campaignIntervalRef.current);
      }
    };
  }, [campaignId, currentCampaign?.status, fetchCampaignById]);

  // Track currently calling contact
  useEffect(() => {
    if (currentCampaign?.contacts) {
      const callingContact = currentCampaign.contacts.find(contact => contact.status === 'calling');
      setCurrentlyCalling(callingContact);
    }
  }, [currentCampaign?.contacts]);

  // Cleanup intervals on unmount
  useEffect(() => {
    return () => {
      if (statusIntervalRef.current) {
        clearInterval(statusIntervalRef.current);
      }
      if (campaignIntervalRef.current) {
        clearInterval(campaignIntervalRef.current);
      }
    };
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadStatus({ message: '', type: '' });
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
      // Refresh campaign data after upload
      await fetchCampaignById(campaignId);
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      setUploadStatus({ message: `Upload failed: ${errorMessage}`, type: 'error' });
    }
  };
  
  const handleStart = async () => {
    setIsStarting(true);
    try {
      await startCampaign(campaignId);
      // Refresh campaign data after starting
      await fetchCampaignById(campaignId);
      setUploadStatus({ message: 'Campaign started successfully! Calls will begin shortly...', type: 'success' });
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      setUploadStatus({ message: `Failed to start campaign: ${errorMessage}`, type: 'error' });
    } finally {
      setIsStarting(false);
    }
  };

  const handleStop = async () => {
    try {
      await stopCampaign(campaignId);
      // Refresh campaign data after stopping
      await fetchCampaignById(campaignId);
      setUploadStatus({ message: 'Campaign paused successfully!', type: 'success' });
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      setUploadStatus({ message: `Failed to stop campaign: ${errorMessage}`, type: 'error' });
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return '#6c757d';
      case 'calling': return '#ffc107';
      case 'completed': return '#28a745';
      case 'failed': return '#dc3545';
      default: return '#6c757d';
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="card">
        <p>Loading campaign details...</p>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="card">
        <p className="error-message">Error: {error}</p>
        <Button onClick={() => fetchCampaignById(campaignId)}>Retry</Button>
      </div>
    );
  }

  // No campaign found
  if (!currentCampaign) {
    return (
      <div className="card">
        <p>Campaign not found.</p>
        <Button onClick={() => fetchCampaignById(campaignId)}>Retry</Button>
      </div>
    );
  }

  return (
    <div>
      <Link to="/campaigns" className="back-link">← Back to Campaigns</Link>
      
      <div className="page-header">
        <h1>{currentCampaign.name}</h1>
        <div className="campaign-actions">
          <Button 
            onClick={handleStop} 
            className="secondary-button"
            disabled={currentCampaign.status !== 'running'}
          >
            Pause
          </Button>
          <Button 
            onClick={handleStart} 
            disabled={currentCampaign.status === 'running' || isStarting}
          >
            {isStarting ? 'Starting...' : 'Start Campaign'}
          </Button>
        </div>
      </div>

      {/* Real-time status indicator */}
      {currentCampaign.status === 'running' && (
        <div className="live-indicator">
          <div className="pulse-dot"></div>
          <span>🔄 Live Updates Active - Refreshing every 3-5 seconds</span>
        </div>
      )}

      {/* Currently calling indicator */}
      {currentlyCalling && (
        <div className="card" style={{ 
          backgroundColor: '#fff3cd', 
          border: '1px solid #ffeaa7',
          marginBottom: '1rem'
        }}>
          <p style={{ margin: 0, color: '#856404', fontWeight: 'bold' }}>
            📞 Currently calling: {currentlyCalling.phone_number}
          </p>
        </div>
      )}

      <div className="campaign-stats card">
        <div><strong>Status:</strong> <span className={`status-badge status-${currentCampaign.status.toLowerCase()}`}>{currentCampaign.status}</span></div>
        <div><strong>Agent ID:</strong> {currentCampaign.agent_id}</div>
        <div><strong>Contacts:</strong> {currentCampaign.contacts.length}</div>
      </div>

      {/* Campaign Status Breakdown */}
      {campaignStatus && (
        <div className="card">
          <h2>Call Progress</h2>
          
          {/* Test Mode Indicator */}
          {campaignStatus.mode === 'TEST' && (
            <div style={{ 
              backgroundColor: '#fff3cd', 
              border: '1px solid #ffeaa7', 
              borderRadius: '6px', 
              padding: '1rem', 
              marginBottom: '1rem' 
            }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#856404' }}>🧪 TEST MODE</h4>
              <p style={{ margin: 0, color: '#856404', fontSize: '0.9rem' }}>
                Running in test mode. Calls are simulated for development purposes.
              </p>
            </div>
          )}
          
          <div className="status-breakdown">
            {Object.entries(campaignStatus.status_breakdown || {}).map(([status, count]) => (
              <div key={status} className="status-item">
                <span 
                  className="status-dot" 
                  style={{ backgroundColor: getStatusColor(status) }}
                ></span>
                <span className="status-label">{status}</span>
                <span className="status-count">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="card">
        <h2>Manage Contacts</h2>
        <div className="upload-section">
          <p>Upload a CSV file with a 'phone_number' column to add contacts.</p>
          <input type="file" accept=".csv" onChange={handleFileChange} />
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
                <tr 
                  key={contact.id}
                  className={contact.status === 'calling' ? 'status-updated' : ''}
                >
                  <td>
                    {contact.phone_number}
                    {contact.status === 'calling' && (
                      <span style={{ marginLeft: '0.5rem', color: '#ffc107' }}>📞</span>
                    )}
                  </td>
                  <td>
                    <span 
                      className={`status-badge status-${contact.status.toLowerCase()}`}
                      style={{ backgroundColor: getStatusColor(contact.status) }}
                    >
                      {contact.status}
                    </span>
                  </td>
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