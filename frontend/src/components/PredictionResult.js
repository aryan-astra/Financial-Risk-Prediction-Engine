'use client';

/**
 * PredictionResult  -  Displays the ML model's prediction output.
 * Shows risk level, probability gauge, explanation text,
 * and top contributing features.
 */
export default function PredictionResult({ result }) {
  if (!result) return null;

  const { risk_level, probability, explanation, top_features, customer_id } = result;

  // Color mapping for risk levels
  const levelColors = {
    Low: { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-700', bar: 'bg-green-500' },
    Medium: { bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-700', bar: 'bg-orange-500' },
    High: { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-700', bar: 'bg-red-500' },
  };

  const colors = levelColors[risk_level] || levelColors.Low;

  return (
    <div className="card">
      <div className="card-header">Prediction Result</div>

      {/* Risk Level Banner */}
      <div className={`${colors.bg} ${colors.border} border rounded-lg p-4 mb-4`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-500">
              {customer_id ? `Customer: ${customer_id}` : 'Assessment Result'}
            </p>
            <p className={`text-2xl font-bold ${colors.text}`}>
              {risk_level} Risk
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-500">Default Probability</p>
            <p className={`text-3xl font-bold ${colors.text}`}>
              {(probability * 100).toFixed(1)}%
            </p>
          </div>
        </div>

        {/* Probability bar */}
        <div className="mt-3 w-full bg-gray-200 rounded-full h-3">
          <div
            className={`${colors.bar} h-3 rounded-full transition-all duration-700`}
            style={{ width: `${Math.min(probability * 100, 100)}%` }}
          />
        </div>
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>0%</span>
          <span>50%</span>
          <span>100%</span>
        </div>
      </div>

      {/* Explanation */}
      <div className="mb-4 p-3 bg-blue-50 border border-blue-100 rounded-lg">
        <p className="text-sm font-medium text-blue-800 mb-1"> Explanation</p>
        <p className="text-sm text-blue-700">{explanation}</p>
      </div>

      {/* Suggested Intervention */}
      {risk_level === 'High' && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm font-medium text-red-800 mb-1"> Recommended Action</p>
          <p className="text-sm text-red-700">
            Immediate outreach recommended: Contact customer to offer payment restructuring,
            payment holiday, or financial counseling before payment is missed.
          </p>
        </div>
      )}

      {risk_level === 'Medium' && (
        <div className="mb-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
          <p className="text-sm font-medium text-orange-800 mb-1"> Recommended Action</p>
          <p className="text-sm text-orange-700">
            Proactive engagement: Send reminder about available support services and
            flexible payment options.
          </p>
        </div>
      )}

      {/* Top Features */}
      {top_features && top_features.length > 0 && (
        <div>
          <p className="text-sm font-medium text-gray-700 mb-2">Top Contributing Factors</p>
          <div className="space-y-2">
            {top_features.map((feat, idx) => (
              <div key={idx} className="flex items-center gap-3 text-sm">
                <span className="w-5 h-5 rounded-full bg-gray-100 flex items-center justify-center text-xs font-medium text-gray-500">
                  {idx + 1}
                </span>
                <span className="font-medium text-gray-700 w-48">
                  {feat.feature?.replace(/_/g, ' ')}
                </span>
                <span className="text-gray-500">
                  = {feat.actual_value}
                </span>
                {feat.direction && (
                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                    feat.direction === 'increases risk'
                      ? 'bg-red-100 text-red-600'
                      : 'bg-green-100 text-green-600'
                  }`}>
                    {feat.direction === 'increases risk' ? '^ risk' : 'v risk'}
                  </span>
                )}
                {feat.shap_value !== undefined && feat.shap_value !== null && (
                  <span className="text-xs text-gray-400">
                    SHAP: {feat.shap_value > 0 ? '+' : ''}{feat.shap_value.toFixed(3)}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
