// SkeletonTableRow.jsx
import React from 'react';
import './SkeletonTableRow.css';

const SkeletonTableRow = () => {
  return (
    <tr className="skeleton-row">
      <td><div className="skeleton-cell"></div></td>
      <td><div className="skeleton-cell"></div></td>
      <td><div className="skeleton-cell"></div></td>
      <td><div className="skeleton-cell"></div></td>
    </tr>
  );
};

export default SkeletonTableRow;
