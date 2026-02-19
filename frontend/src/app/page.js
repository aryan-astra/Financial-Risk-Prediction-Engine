'use client';

import { useState } from 'react';
import StatsCards from '@/components/StatsCards';
import CustomerForm from '@/components/CustomerForm';
import PredictionResult from '@/components/PredictionResult';
import RiskScoreTable from '@/components/RiskScoreTable';
import RiskChart from '@/components/RiskChart';
import AlertPanel from '@/components/AlertPanel';

/**
 * Dashboard Page  -  Main entry point for the Pre-Delinquency Intervention Engine.
 *
 * Layout matches the wireframe:
 *   +------------------------------------------+
 *   |           Stats Cards (top bar)           |
 *   +------------------------------------------+
 *   |           Risk Score Table               |
 *   +--------------------+---------------------+
 *   |   Customer Details  |  Charts / Alerts    |
 *   |   + Prediction      |                     |
 *   +--------------------+---------------------+
 */
export default function DashboardPage() {
  // State to hold the latest prediction result
  const [predictionResult, setPredictionResult] = useState(null);
  // Key to trigger refresh of dashboard components after new prediction
  const [refreshKey, setRefreshKey] = useState(0);

  const handlePrediction = (result) => {
    setPredictionResult(result);
    // Increment key to refresh tables and charts
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="space-y-6">
      {/* Row 1: Stats Overview */}
      <StatsCards refreshKey={refreshKey} />

      {/* Row 2: Risk Score Table (full width) */}
      <RiskScoreTable refreshKey={refreshKey} />

      {/* Row 3: Customer Details (left) + Charts/Alerts (right) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Customer Input + Prediction Result */}
        <div className="space-y-6">
          <CustomerForm onPrediction={handlePrediction} />
          <PredictionResult result={predictionResult} />
        </div>

        {/* Right Column: Charts + Alerts */}
        <div className="space-y-6">
          <RiskChart refreshKey={refreshKey} />
          <AlertPanel refreshKey={refreshKey} />
        </div>
      </div>
    </div>
  );
}
