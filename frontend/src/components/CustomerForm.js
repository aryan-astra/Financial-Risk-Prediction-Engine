'use client';

import { useState } from 'react';
import { predictRisk } from '@/lib/api';

/**
 * Feature input definitions with metadata for form generation.
 * Each entry defines label, key, min, max, step, default, and tooltip.
 */
const FEATURES = [
  { key: 'salary_delay_days', label: 'Salary Delay (days)', min: 0, max: 30, step: 0.5, default: 0, tip: 'Days salary was credited late vs usual' },
  { key: 'balance_trend', label: 'Balance Trend (%)', min: -50, max: 20, step: 0.5, default: 0, tip: 'Week-over-week savings balance change' },
  { key: 'bill_payment_delay', label: 'Bill Pay Delay (days)', min: 0, max: 30, step: 0.5, default: 0, tip: 'Average days bills paid after due date' },
  { key: 'transaction_anomaly', label: 'Transaction Anomaly', min: 0, max: 5, step: 0.1, default: 0, tip: 'Z-score of spending deviation' },
  { key: 'discretionary_drop_pct', label: 'Discretionary Drop (%)', min: 0, max: 100, step: 1, default: 0, tip: 'Decline in discretionary spending' },
  { key: 'atm_withdrawal_spike', label: 'ATM Withdrawal Spike', min: 0.5, max: 5, step: 0.1, default: 1.0, tip: 'Ratio vs 3-month average' },
  { key: 'failed_auto_debits', label: 'Failed Auto-Debits', min: 0, max: 5, step: 1, default: 0, tip: 'Failed auto-debit attempts last month' },
  { key: 'lending_app_txns', label: 'Lending App Txns', min: 0, max: 20, step: 1, default: 0, tip: 'UPI txns to lending apps' },
  { key: 'savings_drawdown_pct', label: 'Savings Drawdown (%)', min: 0, max: 100, step: 1, default: 0, tip: 'Savings drawn down in last 30d' },
  { key: 'credit_utilization', label: 'Credit Utilization (%)', min: 0, max: 100, step: 1, default: 0, tip: 'Credit card utilization' },
];

/**
 * CustomerForm  -  Input form for customer financial signals.
 * Submits data to the backend prediction API and passes results
 * to the parent component via onPrediction callback.
 */
export default function CustomerForm({ onPrediction }) {
  // Initialize form state with defaults
  const initialState = {
    customer_id: '',
    name: '',
    ...Object.fromEntries(FEATURES.map(f => [f.key, f.default])),
  };

  const [formData, setFormData] = useState(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Convert numeric fields to proper types
      const payload = {
        ...formData,
        customer_id: formData.customer_id || undefined,
        name: formData.name || undefined,
      };
      FEATURES.forEach(f => {
        payload[f.key] = Number(payload[f.key]);
      });

      const result = await predictRisk(payload);
      onPrediction(result);
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Prediction failed';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData(initialState);
    setError(null);
  };

  // Quick-fill presets for demo  -  realistic Indian customer profiles
  const fillHighRisk = () => {
    setFormData({
      customer_id: 'CUST-000005',
      name: 'Vikram Reddy',
      salary_delay_days: 20,
      balance_trend: -40,
      bill_payment_delay: 25,
      transaction_anomaly: 4.5,
      discretionary_drop_pct: 75,
      atm_withdrawal_spike: 4.0,
      failed_auto_debits: 5,
      lending_app_txns: 12,
      savings_drawdown_pct: 85,
      credit_utilization: 95,
    });
  };

  const fillMediumRisk = () => {
    setFormData({
      customer_id: 'CUST-000004',
      name: 'Neha Patel',
      salary_delay_days: 8,
      balance_trend: -15,
      bill_payment_delay: 10,
      transaction_anomaly: 1.8,
      discretionary_drop_pct: 35,
      atm_withdrawal_spike: 2.0,
      failed_auto_debits: 1,
      lending_app_txns: 4,
      savings_drawdown_pct: 30,
      credit_utilization: 55,
    });
  };

  const fillLowRisk = () => {
    setFormData({
      customer_id: 'CUST-000003',
      name: 'Amit Singh',
      salary_delay_days: 0,
      balance_trend: 5,
      bill_payment_delay: 1,
      transaction_anomaly: 0.2,
      discretionary_drop_pct: 3,
      atm_withdrawal_spike: 0.7,
      failed_auto_debits: 0,
      lending_app_txns: 0,
      savings_drawdown_pct: 2,
      credit_utilization: 15,
    });
  };

  return (
    <div className="card">
      <div className="card-header flex items-center justify-between">
        <span>Customer Details</span>
        <div className="flex gap-2">
          <button onClick={fillLowRisk} className="text-xs bg-green-50 text-green-600 px-2 py-1 rounded hover:bg-green-100 transition-colors">
            Amit Singh (Low)
          </button>
          <button onClick={fillMediumRisk} className="text-xs bg-yellow-50 text-yellow-600 px-2 py-1 rounded hover:bg-yellow-100 transition-colors">
            Neha Patel (Medium)
          </button>
          <button onClick={fillHighRisk} className="text-xs bg-red-50 text-red-600 px-2 py-1 rounded hover:bg-red-100 transition-colors">
            Vikram Reddy (High)
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Customer identity */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div>
            <label className="form-label">Customer ID</label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g., CUST-00001"
              value={formData.customer_id}
              onChange={(e) => handleChange('customer_id', e.target.value)}
            />
          </div>
          <div>
            <label className="form-label">Name</label>
            <input
              type="text"
              className="form-input"
              placeholder="Customer name"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
            />
          </div>
        </div>

        {/* Feature inputs */}
        <div className="grid grid-cols-2 gap-3 mb-5">
          {FEATURES.map((f) => (
            <div key={f.key}>
              <label className="form-label" title={f.tip}>
                {f.label}
              </label>
              <input
                type="number"
                className="form-input"
                min={f.min}
                max={f.max}
                step={f.step}
                value={formData[f.key]}
                onChange={(e) => handleChange(f.key, e.target.value)}
                required
              />
            </div>
          ))}
        </div>

        {/* Error message */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
            {error}
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          <button type="submit" className="btn-primary flex items-center gap-2" disabled={loading}>
            {loading && <span className="spinner" />}
            {loading ? 'Predicting...' : 'Predict Risk'}
          </button>
          <button type="button" onClick={handleReset} className="btn-secondary">
            Reset
          </button>
        </div>
      </form>
    </div>
  );
}
