/**
 * API Client  -  Centralized backend communication
 *
 * All calls go through the Next.js rewrite proxy (/api/... -> localhost:8000/api/...)
 * so we avoid CORS issues in development.
 */
import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 15000,
});

// ---- Prediction ----

/**
 * Submit customer features and get risk prediction.
 * @param {Object} features - Customer financial signal values
 * @returns {Object} Prediction result with risk level, probability, explanation
 */
export async function predictRisk(features) {
  const response = await api.post('/api/predict/', features);
  return response.data;
}

/**
 * Get global feature importance from the trained model.
 */
export async function getFeatureImportance() {
  const response = await api.get('/api/predict/feature-importance');
  return response.data;
}

// ---- Dashboard ----

/**
 * Get overall dashboard statistics.
 */
export async function getDashboardStats() {
  const response = await api.get('/api/dashboard/stats');
  return response.data;
}

/**
 * Get recent predictions for the risk score table.
 * @param {number} limit - Number of records to fetch
 */
export async function getRecentPredictions(limit = 20) {
  const response = await api.get(`/api/dashboard/recent-predictions?limit=${limit}`);
  return response.data;
}

/**
 * Get risk distribution data for charts.
 */
export async function getRiskDistribution() {
  const response = await api.get('/api/dashboard/risk-distribution');
  return response.data;
}

/**
 * Get high-risk alerts.
 */
export async function getAlerts(limit = 10) {
  const response = await api.get(`/api/dashboard/alerts?limit=${limit}`);
  return response.data;
}

// ---- Customers ----

/**
 * List customers with pagination.
 */
export async function getCustomers(skip = 0, limit = 50) {
  const response = await api.get(`/api/customers/?skip=${skip}&limit=${limit}`);
  return response.data;
}

export default api;
