'use client';

import { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from 'recharts';
import { getRiskDistribution, getFeatureImportance } from '@/lib/api';

/**
 * RiskChart  -  Visualizations for the dashboard.
 * Shows risk distribution (bar + pie) and feature importance.
 * Refreshes when refreshKey changes.
 */

const RISK_COLORS = {
  Low: '#4CAF50',
  Medium: '#FF9800',
  High: '#F44336',
};

export default function RiskChart({ refreshKey }) {
  const [distribution, setDistribution] = useState(null);
  const [featureImp, setFeatureImp] = useState(null);
  const [activeTab, setActiveTab] = useState('distribution');

  useEffect(() => {
    fetchData();
  }, [refreshKey]);

  const fetchData = async () => {
    try {
      const [dist, feat] = await Promise.all([
        getRiskDistribution(),
        getFeatureImportance(),
      ]);
      setDistribution(dist);
      setFeatureImp(feat);
    } catch (err) {
      console.error('Failed to fetch chart data:', err);
    }
  };

  // Prepare data for Recharts
  const barData = distribution
    ? distribution.labels.map((label, i) => ({
        name: label,
        count: distribution.values[i],
        fill: distribution.colors[i],
      }))
    : [];

  const pieData = distribution
    ? distribution.labels.map((label, i) => ({
        name: label,
        value: distribution.values[i],
      }))
    : [];

  const featureData = featureImp
    ? featureImp.slice(0, 8).map(f => ({
        name: f.feature.replace(/_/g, ' '),
        importance: +(f.importance * 100).toFixed(1),
      }))
    : [];

  const totalPredictions = barData.reduce((sum, d) => sum + d.count, 0);

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex gap-4">
          {['distribution', 'features'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`text-sm pb-1 border-b-2 transition-colors ${
                activeTab === tab
                  ? 'border-blue-500 text-blue-600 font-medium'
                  : 'border-transparent text-gray-400 hover:text-gray-600'
              }`}
            >
              {tab === 'distribution' ? 'Risk Distribution' : 'Feature Importance'}
            </button>
          ))}
        </div>
      </div>

      {totalPredictions === 0 && activeTab === 'distribution' ? (
        <div className="text-center py-8 text-gray-400">
          <p className="text-sm">No data available yet. Run predictions to see charts.</p>
        </div>
      ) : (
        <>
          {activeTab === 'distribution' && (
            <div className="grid grid-cols-2 gap-4">
              {/* Bar Chart */}
              <div>
                <p className="text-xs text-gray-500 mb-2 text-center">Count by Risk Level</p>
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={barData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                    <YAxis tick={{ fontSize: 12 }} />
                    <Tooltip />
                    <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                      {barData.map((entry, idx) => (
                        <Cell key={idx} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Pie Chart */}
              <div>
                <p className="text-xs text-gray-500 mb-2 text-center">Distribution %</p>
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      innerRadius={50}
                      outerRadius={80}
                      dataKey="value"
                      label={({ name, percent }) =>
                        `${name} ${(percent * 100).toFixed(0)}%`
                      }
                      labelLine={false}
                    >
                      {pieData.map((entry, idx) => (
                        <Cell
                          key={idx}
                          fill={RISK_COLORS[entry.name] || '#ccc'}
                        />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {activeTab === 'features' && featureData.length > 0 && (
            <div>
              <p className="text-xs text-gray-500 mb-2">
                Model feature importance (higher = more influence on predictions)
              </p>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={featureData} layout="vertical" margin={{ left: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis type="number" tick={{ fontSize: 11 }} unit="%" />
                  <YAxis
                    type="category"
                    dataKey="name"
                    width={140}
                    tick={{ fontSize: 11 }}
                  />
                  <Tooltip formatter={(val) => `${val}%`} />
                  <Bar dataKey="importance" fill="#00AEEF" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </>
      )}
    </div>
  );
}
