# -------------------------------------------------
# models.py  -  SQLAlchemy ORM Models
# -------------------------------------------------
# Defines the database schema for customer records
# and prediction results.
# -------------------------------------------------

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, Boolean
)
from sqlalchemy.sql import func
from database import Base


class Customer(Base):
    """
    Stores customer financial signal snapshots.
    Each row is a point-in-time capture of behavioral indicators.
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=True)

    # Indian identity / demographic fields
    gender = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)
    phone = Column(String(20), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    pan_number = Column(String(15), nullable=True)
    aadhaar_masked = Column(String(20), nullable=True)
    account_number = Column(String(20), nullable=True)
    ifsc_code = Column(String(15), nullable=True)
    bank_branch = Column(String(50), nullable=True)
    occupation = Column(String(50), nullable=True)
    monthly_income_inr = Column(Integer, default=0)
    loan_type = Column(String(30), nullable=True)
    loan_amount_inr = Column(Integer, default=0)
    emi_amount_inr = Column(Integer, default=0)
    loan_tenure_months = Column(Integer, default=0)
    active_loans = Column(Integer, default=1)
    emi_to_income_ratio = Column(Float, default=0)
    upi_txn_count = Column(Integer, default=0)

    # Financial stress signals (core ML features)
    salary_delay_days = Column(Float, default=0)
    balance_trend = Column(Float, default=0)
    bill_payment_delay = Column(Float, default=0)
    transaction_anomaly = Column(Float, default=0)
    discretionary_drop_pct = Column(Float, default=0)
    atm_withdrawal_spike = Column(Float, default=1.0)
    failed_auto_debits = Column(Integer, default=0)
    lending_app_txns = Column(Integer, default=0)
    savings_drawdown_pct = Column(Float, default=0)
    credit_utilization = Column(Float, default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class PredictionResult(Base):
    """
    Stores model prediction results for each customer assessment.
    Links to a customer and includes risk score + explanation.
    """
    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(20), nullable=False, index=True)

    # Prediction outputs
    risk_probability = Column(Float, nullable=False)
    risk_level = Column(String(10), nullable=False)  # Low, Medium, High
    prediction = Column(Integer, nullable=False)       # 0 or 1

    # Explanation
    explanation = Column(Text, nullable=True)
    top_features_json = Column(Text, nullable=True)  # JSON string of top features

    # Alert tracking
    alert_sent = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
