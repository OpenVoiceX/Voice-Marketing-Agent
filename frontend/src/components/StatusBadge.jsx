// frontend/src/components/StatusBadge.jsx
import React from 'react';

const StatusBadge = ({ status, lastCallTime }) => {
  const getStatusConfig = (status) => {
    switch (status) {
      case 'completed':
        return {
          color: 'bg-green-100 text-green-800 border-green-200',
          icon: '✓',
          label: 'Completed'
        };
      case 'failed':
        return {
          color: 'bg-red-100 text-red-800 border-red-200',
          icon: '✗',
          label: 'Failed'
        };
      case 'in_progress':
        return {
          color: 'bg-blue-100 text-blue-800 border-blue-200',
          icon: '⟳',
          label: 'In Progress'
        };
      case 'idle':
      default:
        return {
          color: 'bg-gray-100 text-gray-600 border-gray-200',
          icon: '○',
          label: 'Idle'
        };
    }
  };

  const config = getStatusConfig(status);
  
  const formatTime = (timeString) => {
    if (!timeString) return '';
    const date = new Date(timeString);
    return date.toLocaleString();
  };

  return (
    <div className="flex items-center space-x-2">
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${config.color}`}>
        <span className="mr-1">{config.icon}</span>
        Last Call: {config.label}
      </span>
      {lastCallTime && (
        <span className="text-xs text-gray-500">
          {formatTime(lastCallTime)}
        </span>
      )}
    </div>
  );
};

export default StatusBadge;