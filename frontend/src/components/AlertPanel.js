'use client';

import { useEffect, useState } from 'react';
import { getAlerts } from '@/lib/api';

/**
 * AlertPanel  -  Displays high-risk customer alerts.
 * Shows recent alerts with suggested interventions.
 * Refreshes when refreshKey changes.
 */
export default function AlertPanel({ refreshKey }) {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
  }, [refreshKey]);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const data = await getAlerts(10);
      setAlerts(data);
    } catch (err) {
      console.error('Failed to fetch alerts:', err);
      setAlerts([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card">
        <div className="card-header"> Alerts</div>
        <div className="flex items-center justify-center py-6">
          <span className="spinner mr-2" />
          <span className="text-gray-500 text-sm">Loading alerts...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header flex items-center justify-between">
        <span> Alerts</span>
        {alerts.length > 0 && (
          <span className="text-xs bg-red-100 text-red-600 px-2 py-0.5 rounded-full">
            {alerts.length} high-risk
          </span>
        )}
      </div>

      {alerts.length === 0 ? (
        <div className="text-center py-6 text-gray-400">
          <p className="text-2xl mb-1">[OK]</p>
          <p className="text-sm">No high-risk alerts</p>
        </div>
      ) : (
        <div className="space-y-3 max-h-80 overflow-y-auto">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className="p-3 bg-red-50 border border-red-100 rounded-lg"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-red-800">
                  {alert.customer_name || alert.customer_id}
                </span>
                <span className="text-xs text-red-500 font-medium">
                  {(alert.risk_probability * 100).toFixed(1)}% risk
                </span>
              </div>
              <p className="text-xs text-red-600 mb-1.5">{alert.explanation}</p>
              <div className="bg-red-100/50 rounded p-2">
                <p className="text-xs text-red-700">
                  <strong>Action:</strong> {alert.suggested_action}
                </p>
              </div>
              <p className="text-xs text-gray-400 mt-1">
                {alert.created_at
                  ? new Date(alert.created_at).toLocaleString()
                  : ''}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
