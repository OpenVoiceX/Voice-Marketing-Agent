// frontend/src/components/CampaignDetail.jsx
import React from 'react';

const CampaignDetail = ({ campaign }) => {
  if (!campaign) return null;

  return (
    <div className="mt-4 border p-2">
      <h2>Campaign: {campaign.name}</h2>
      <h3>Status: {campaign.status}</h3>
      <h4>Contacts:</h4>
      <ul>
        {campaign.contacts?.map((contact) => (
          <li key={contact.id}>
            {contact.name} - {contact.callStatus}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CampaignDetail;
