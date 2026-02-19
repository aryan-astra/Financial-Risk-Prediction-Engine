'use client';

import { useEffect, useState } from 'react';
import { getRecentPredictions } from '@/lib/api';

/**
 * RiskScoreTable  -  Displays recent prediction results in a table.
 * Shows customer ID, name, risk level, probability, and time.
 * Refreshes when refreshKey prop changes.
 */
export default function RiskScoreTable({ refreshKey }) {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPredictions();
  }, [refreshKey]);

  const fetchPredictions = async () => {
    try {
      setLoading(true);
      const data = await getRecentPredictions(20);
      setPredictions(data);
    } catch (err) {
      console.error('Failed to fetch predictions:', err);
      // Show empty state on error
      setPredictions([]);
    } finally {
      setLoading(false);
    }
  };

  const getBadgeClass = (level) => {
    switch (level) {
      case 'High': return 'badge badge-high';
      case 'Medium': return 'badge badge-medium';
      default: return 'badge badge-low';
    }
  };

  if (loading) {
    return (
      <div className="card">
        <div className="card-header">Risk Score Table</div>
        <div className="flex items-center justify-center py-8">
          <span className="spinner mr-2" />
          <span className="text-gray-500 text-sm">Loading predictions...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header flex items-center justify-between">
        <span>Risk Score Table</span>
        <span className="text-xs text-gray-400">{predictions.length} records</span>
      </div>

      {predictions.length === 0 ? (
        <div className="text-center py-8 text-gray-400">
          <p className="text-base mb-1">No predictions yet</p>
          <p className="text-sm">Submit customer data to see results here</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>Customer ID</th>
                <th>Name</th>
                <th>Risk Level</th>
                <th>Probability</th>
                <th>Alert</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((pred) => (
                <tr key={pred.id}>
                  <td className="font-mono text-xs">{pred.customer_id}</td>
                  <td>{pred.customer_name || ' - '}</td>
                  <td>
                    <span className={getBadgeClass(pred.risk_level)}>
                      {pred.risk_level}
                    </span>
                  </td>
                  <td className="font-medium">
                    {(pred.risk_probability * 100).toFixed(1)}%
                  </td>
                  <td>
                    {pred.alert_sent ? (
                      <span className="text-red-500 text-xs font-medium"> Sent</span>
                    ) : (
                      <span className="text-gray-300 text-xs"> - </span>
                    )}
                  </td>
                  <td className="text-xs text-gray-400">
                    {pred.created_at
                      ? new Date(pred.created_at).toLocaleString()
                      : ' - '}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
