'use client';

import { useEffect, useState } from 'react';
import { getDashboardStats } from '@/lib/api';

/**
 * StatsCards  -  Top-level stat summary cards for the dashboard.
 * Shows total customers, predictions, risk distribution, alerts.
 */
export default function StatsCards({ refreshKey }) {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchStats();
  }, [refreshKey]);

  const fetchStats = async () => {
    try {
      const data = await getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    }
  };

  if (!stats) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="stat-card animate-pulse">
            <div className="w-16 h-8 bg-gray-200 rounded mb-2" />
            <div className="w-24 h-4 bg-gray-100 rounded" />
          </div>
        ))}
      </div>
    );
  }

  const cards = [
    {
      label: 'Total Customers',
      value: stats.total_customers,
      color: 'text-blue-600',
      icon: '',
    },
    {
      label: 'Predictions Made',
      value: stats.total_predictions,
      color: 'text-purple-600',
      icon: '',
    },
    {
      label: 'Avg Risk Score',
      value: `${(stats.avg_risk_probability * 100).toFixed(1)}%`,
      color: stats.avg_risk_probability > 0.5 ? 'text-red-600' : 'text-green-600',
      icon: '',
    },
    {
      label: 'Active Alerts',
      value: stats.alerts_pending,
      color: stats.alerts_pending > 0 ? 'text-red-600' : 'text-green-600',
      icon: '',
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((card, idx) => (
        <div key={idx} className="stat-card">
          <span className="text-2xl mb-1">{card.icon}</span>
          <span className={`stat-value ${card.color}`}>{card.value}</span>
          <span className="stat-label">{card.label}</span>
        </div>
      ))}
    </div>
  );
}
