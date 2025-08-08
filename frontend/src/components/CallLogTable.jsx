// frontend/src/components/CallLogTable.jsx

import React, { useEffect, useState } from 'react';
import SkeletonTableRow from './common/SkeletonTableRow';

const CallLogTable = () => {
  const [loading, setLoading] = useState(true);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLogs([
        {
          id: 1,
          sid: 'CA123...',
          from: '+15551234567',
          startTime: '2023-10-27 10:00 AM',
          status: 'Completed'
        },
        {
          id: 2,
          sid: 'CA456...',
          from: '+15557654321',
          startTime: '2023-10-27 10:05 AM',
          status: 'In Progress'
        }
      ]);
      setLoading(false);
    }, 3000); // Simulate 3s API delay

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="card">
      <h2>Recent Calls</h2>

      <table>
        <thead>
          <tr>
            <th>Call SID</th>
            <th>From</th>
            <th>Start Time</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <>
              <SkeletonTableRow />
              <SkeletonTableRow />
              <SkeletonTableRow />
            </>
          ) : (
            logs.map((log) => (
              <tr key={log.id}>
                <td>{log.sid}</td>
                <td>{log.from}</td>
                <td>{log.startTime}</td>
                <td>{log.status}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default CallLogTable;
