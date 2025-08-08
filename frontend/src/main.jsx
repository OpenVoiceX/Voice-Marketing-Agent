// frontend/src/main.jsx
import CallLogTable from './components/CallLogTable.jsx';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App.jsx';
import './assets/index.css';

import DashboardPage from './pages/DashboardPage.jsx';
import AgentsPage from './pages/AgentsPage.jsx';
import AgentDetailPage from './pages/AgentDetailPage.jsx';
import CampaignsPage from './pages/CampaignsPage.jsx';
import CampaignDetailPage from './pages/CampaignDetailPage.jsx'; // <-- IMPORT NEW PAGE

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "agents", element: <AgentsPage /> },
      { path: "agents/:agentId", element: <AgentDetailPage /> },
      { path: "campaigns", element: <CampaignsPage /> },
      { path: "calls", element: <CallLogTable /> },
      // --- ADD THIS NEW DYNAMIC ROUTE ---
      {
        path: "campaigns/:campaignId",
        element: <CampaignDetailPage />,
      },
      // -----------------------------------
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);