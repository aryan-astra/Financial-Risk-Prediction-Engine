# -------------------------------------------------
# explain.py  -  SHAP Explainability Module
# -------------------------------------------------
# Provides feature-level explanations for model predictions
# using SHAP (SHapley Additive exPlanations). Can generate
# global and local explanations for transparency.
# -------------------------------------------------

import os
import sys
import joblib
import numpy as np
import pandas as pd

# Paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "risk_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

# Feature names
from preprocess import FEATURE_COLUMNS


def load_model_and_scaler():
    """Load the trained model and scaler from disk."""
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


def explain_prediction(features_dict: dict, model=None, scaler=None) -> dict:
    """
    Explain a single prediction using SHAP TreeExplainer.

    Args:
        features_dict: Dictionary of feature name -> value
        model: Trained model (loaded from disk if None)
        scaler: Fitted scaler (loaded from disk if None)

    Returns:
        Dictionary with prediction, probability, risk_level,
        SHAP values, and human-readable explanation.
    """
    if model is None or scaler is None:
        model, scaler = load_model_and_scaler()

    # Prepare input
    input_df = pd.DataFrame([features_dict])[FEATURE_COLUMNS]
    input_scaled = pd.DataFrame(
        scaler.transform(input_df),
        columns=FEATURE_COLUMNS,
    )

    # Predict
    prediction = int(model.predict(input_scaled)[0])
    probability = float(model.predict_proba(input_scaled)[0][1])

    # Determine risk level
    if probability < 0.3:
        risk_level = "Low"
    elif probability < 0.6:
        risk_level = "Medium"
    else:
        risk_level = "High"

    # SHAP explanation
    shap_values_dict = {}
    top_features = []
    explanation_text = ""

    try:
        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_scaled)

        # For binary classification, shap_values is a list [class_0, class_1]
        if isinstance(shap_values, list):
            sv = np.array(shap_values[1][0]).flatten()  # SHAP values for class 1 (default)
        elif shap_values.ndim == 3:
            sv = np.array(shap_values[0, :, 1]).flatten()
        else:
            sv = np.array(shap_values[0]).flatten()

        # Build SHAP values dictionary
        shap_values_dict = {
            col: round(float(sv[i]), 4)
            for i, col in enumerate(FEATURE_COLUMNS)
        }

        # Top contributing features (sorted by absolute SHAP value)
        sorted_feats = sorted(
            shap_values_dict.items(),
            key=lambda x: abs(x[1]),
            reverse=True,
        )
        top_features = [
            {
                "feature": f,
                "shap_value": v,
                "actual_value": round(float(features_dict.get(f, 0)), 2),
                "direction": "increases risk" if v > 0 else "decreases risk",
            }
            for f, v in sorted_feats[:5]
        ]

        # Human-readable explanation
        parts = []
        for tf in top_features[:3]:
            parts.append(
                f"{tf['feature'].replace('_', ' ')} = {tf['actual_value']} "
                f"({tf['direction']})"
            )
        explanation_text = (
            f"Risk level: {risk_level} (probability: {probability:.1%}). "
            f"Top factors: {'; '.join(parts)}."
        )

    except ImportError:
        # SHAP not installed  -  fall back to feature importance
        importances = model.feature_importances_
        feat_imp = sorted(
            zip(FEATURE_COLUMNS, importances),
            key=lambda x: x[1],
            reverse=True,
        )
        top_features = [
            {
                "feature": f,
                "importance": round(float(imp), 4),
                "actual_value": round(float(features_dict.get(f, 0)), 2),
            }
            for f, imp in feat_imp[:5]
        ]
        explanation_text = (
            f"Risk level: {risk_level} (probability: {probability:.1%}). "
            f"SHAP not available  -  using feature importance instead."
        )

    return {
        "prediction": prediction,
        "probability": round(probability, 4),
        "risk_level": risk_level,
        "shap_values": shap_values_dict,
        "top_features": top_features,
        "explanation": explanation_text,
    }


def get_global_feature_importance(model=None) -> list:
    """Return global feature importances from the model."""
    if model is None:
        model, _ = load_model_and_scaler()

    importances = model.feature_importances_
    return sorted(
        [
            {"feature": f, "importance": round(float(imp), 4)}
            for f, imp in zip(FEATURE_COLUMNS, importances)
        ],
        key=lambda x: x["importance"],
        reverse=True,
    )


if __name__ == "__main__":
    # Demo: explain a sample high-risk customer
    sample = {
        "salary_delay_days": 15,
        "balance_trend": -30,
        "bill_payment_delay": 20,
        "transaction_anomaly": 3.5,
        "discretionary_drop_pct": 60,
        "atm_withdrawal_spike": 3.0,
        "failed_auto_debits": 3,
        "lending_app_txns": 8,
        "savings_drawdown_pct": 70,
        "credit_utilization": 85,
    }
    result = explain_prediction(sample)
    print("\n=== Prediction Explanation ===")
    for key, value in result.items():
        print(f"  {key}: {value}")
