# -------------------------------------------------
# routes/predict.py  -  Prediction Endpoints
# -------------------------------------------------
# Handles risk prediction requests: accepts customer
# feature data, runs the ML model, returns risk score
# with explainability details.
# -------------------------------------------------

import sys
import os
import json
import joblib
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Add project paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_db
from models import Customer, PredictionResult
from schemas import PredictionRequest, PredictionResponse
from config import MODEL_PATH, SCALER_PATH

# ML imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ml"))
from preprocess import FEATURE_COLUMNS
from explain import explain_prediction

router = APIRouter(prefix="/api/predict", tags=["Prediction"])

# Load model and scaler at module level for performance
_model = None
_scaler = None


def get_model():
    """Lazy-load the trained model."""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(
                status_code=503,
                detail="Model not found. Please run 'python ml/train.py' first.",
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def get_scaler():
    """Lazy-load the fitted scaler."""
    global _scaler
    if _scaler is None:
        if not os.path.exists(SCALER_PATH):
            raise HTTPException(
                status_code=503,
                detail="Scaler not found. Please run 'python ml/train.py' first.",
            )
        _scaler = joblib.load(SCALER_PATH)
    return _scaler


@router.post("/", response_model=PredictionResponse)
def predict_risk(request: PredictionRequest, db: Session = Depends(get_db)):
    """
    Predict default risk for a customer based on financial signals.

    Accepts feature values, runs the RandomForest model, and returns:
    - Risk probability (0-1)
    - Risk level (Low / Medium / High)
    - Human-readable explanation
    - Top contributing features with SHAP values
    """
    model = get_model()
    scaler = get_scaler()

    # Build feature dictionary from request
    features = {
        "salary_delay_days": request.salary_delay_days,
        "balance_trend": request.balance_trend,
        "bill_payment_delay": request.bill_payment_delay,
        "transaction_anomaly": request.transaction_anomaly,
        "discretionary_drop_pct": request.discretionary_drop_pct,
        "atm_withdrawal_spike": request.atm_withdrawal_spike,
        "failed_auto_debits": request.failed_auto_debits,
        "lending_app_txns": request.lending_app_txns,
        "savings_drawdown_pct": request.savings_drawdown_pct,
        "credit_utilization": request.credit_utilization,
    }

    # Get prediction with explanation
    result = explain_prediction(features, model=model, scaler=scaler)

    # Optionally save customer record and prediction to database
    try:
        customer_id = request.customer_id or f"ANON-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"

        # Upsert customer
        existing = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if existing:
            for key, value in features.items():
                setattr(existing, key, value)
            if request.name:
                existing.name = request.name
        else:
            customer = Customer(
                customer_id=customer_id,
                name=request.name,
                **features,
            )
            db.add(customer)

        # Save prediction
        pred_record = PredictionResult(
            customer_id=customer_id,
            risk_probability=result["probability"],
            risk_level=result["risk_level"],
            prediction=result["prediction"],
            explanation=result["explanation"],
            top_features_json=json.dumps(result["top_features"]),
            alert_sent=result["risk_level"] == "High",
        )
        db.add(pred_record)
        db.commit()
    except Exception as e:
        db.rollback()
        # Don't fail the prediction if DB save fails
        print(f"Warning: Could not save to database: {e}")

    return PredictionResponse(
        customer_id=request.customer_id,
        prediction=result["prediction"],
        probability=result["probability"],
        risk_level=result["risk_level"],
        explanation=result["explanation"],
        top_features=result["top_features"],
        shap_values=result.get("shap_values"),
    )


@router.get("/feature-importance")
def get_feature_importance():
    """Return global feature importance from the trained model."""
    model = get_model()
    importances = model.feature_importances_
    return sorted(
        [
            {"feature": f, "importance": round(float(imp), 4)}
            for f, imp in zip(FEATURE_COLUMNS, importances)
        ],
        key=lambda x: x["importance"],
        reverse=True,
    )
