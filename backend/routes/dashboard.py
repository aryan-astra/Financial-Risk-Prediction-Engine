# -------------------------------------------------
# routes/dashboard.py  -  Dashboard Data Endpoints
# -------------------------------------------------
# Provides aggregated data for the Next.js dashboard:
# risk distribution, recent predictions, alerts, and stats.
# -------------------------------------------------

import sys
import os
import json
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_db
from models import Customer, PredictionResult
from schemas import DashboardStats, RiskDistribution

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Return overall dashboard statistics."""
    total_customers = db.query(Customer).count()
    total_predictions = db.query(PredictionResult).count()

    # Risk distribution
    low = db.query(PredictionResult).filter(PredictionResult.risk_level == "Low").count()
    medium = db.query(PredictionResult).filter(PredictionResult.risk_level == "Medium").count()
    high = db.query(PredictionResult).filter(PredictionResult.risk_level == "High").count()

    # Average risk probability
    avg_prob = db.query(func.avg(PredictionResult.risk_probability)).scalar() or 0.0

    # Pending alerts (high risk, not yet sent)
    alerts_pending = (
        db.query(PredictionResult)
        .filter(PredictionResult.risk_level == "High")
        .filter(PredictionResult.alert_sent == False)
        .count()
    )

    return DashboardStats(
        total_customers=total_customers,
        total_predictions=total_predictions,
        risk_distribution=RiskDistribution(
            low=low, medium=medium, high=high, total=low + medium + high
        ),
        avg_risk_probability=round(float(avg_prob), 4),
        alerts_pending=alerts_pending,
    )


@router.get("/recent-predictions")
def get_recent_predictions(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Return the most recent predictions with customer details."""
    results = (
        db.query(PredictionResult)
        .order_by(PredictionResult.created_at.desc())
        .limit(limit)
        .all()
    )

    predictions = []
    for r in results:
        # Fetch customer name
        customer = db.query(Customer).filter(Customer.customer_id == r.customer_id).first()
        predictions.append({
            "id": r.id,
            "customer_id": r.customer_id,
            "customer_name": customer.name if customer else None,
            "risk_probability": r.risk_probability,
            "risk_level": r.risk_level,
            "prediction": r.prediction,
            "explanation": r.explanation,
            "top_features": json.loads(r.top_features_json) if r.top_features_json else [],
            "alert_sent": r.alert_sent,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        })

    return predictions


@router.get("/risk-distribution")
def get_risk_distribution(db: Session = Depends(get_db)):
    """Return risk level counts for chart visualization."""
    low = db.query(PredictionResult).filter(PredictionResult.risk_level == "Low").count()
    medium = db.query(PredictionResult).filter(PredictionResult.risk_level == "Medium").count()
    high = db.query(PredictionResult).filter(PredictionResult.risk_level == "High").count()

    return {
        "labels": ["Low", "Medium", "High"],
        "values": [low, medium, high],
        "colors": ["#4CAF50", "#FF9800", "#F44336"],
    }


@router.get("/alerts")
def get_alerts(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Return high-risk alerts for the dashboard alert panel."""
    high_risk = (
        db.query(PredictionResult)
        .filter(PredictionResult.risk_level == "High")
        .order_by(PredictionResult.created_at.desc())
        .limit(limit)
        .all()
    )

    alerts = []
    for r in high_risk:
        customer = db.query(Customer).filter(Customer.customer_id == r.customer_id).first()
        alerts.append({
            "id": r.id,
            "customer_id": r.customer_id,
            "customer_name": customer.name if customer else "Unknown",
            "risk_probability": r.risk_probability,
            "explanation": r.explanation,
            "alert_sent": r.alert_sent,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "suggested_action": _suggest_intervention(r.risk_probability),
        })

    return alerts


def _suggest_intervention(probability: float) -> str:
    """Generate a suggested intervention based on risk probability."""
    if probability >= 0.8:
        return "Immediate outreach: Offer payment restructuring or payment holiday"
    elif probability >= 0.6:
        return "Proactive contact: Suggest financial counseling and flexible payment options"
    else:
        return "Monitor closely: Send gentle reminder about available support services"
