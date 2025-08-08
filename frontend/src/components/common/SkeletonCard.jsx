// frontend/src/components/common/SkeletonCard.jsx
import React from 'react';
import './SkeletonCard.css';

const SkeletonCard = () => {
  return (
    <div className="skeleton-card">
      <div className="skeleton-avatar"></div>
      <div className="skeleton-line short"></div>
      <div className="skeleton-line"></div>
    </div>
  );
};

export default SkeletonCard;
