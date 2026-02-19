# -------------------------------------------------
# schemas.py  -  Pydantic Request/Response Schemas
# -------------------------------------------------
# Defines the data shapes for API request validation
# and response serialization.
# -------------------------------------------------

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ---- Prediction ----

class PredictionRequest(BaseModel):
    """Input features for risk prediction."""
    customer_id: Optional[str] = Field(None, description="Customer identifier")
    name: Optional[str] = Field(None, description="Customer name")
    salary_delay_days: float = Field(..., ge=0, le=30, description="Days salary was delayed")
    balance_trend: float = Field(..., ge=-50, le=20, description="Week-over-week balance change %")
    bill_payment_delay: float = Field(..., ge=0, le=30, description="Average bill payment delay in days")
    transaction_anomaly: float = Field(..., ge=0, le=5, description="Transaction anomaly z-score")
    discretionary_drop_pct: float = Field(..., ge=0, le=100, description="Discretionary spending drop %")
    atm_withdrawal_spike: float = Field(..., ge=0.5, le=5, description="ATM withdrawal spike ratio")
    failed_auto_debits: int = Field(..., ge=0, le=5, description="Failed auto-debit attempts")
    lending_app_txns: int = Field(..., ge=0, le=20, description="Lending app transactions count")
    savings_drawdown_pct: float = Field(..., ge=0, le=100, description="Savings drawdown %")
    credit_utilization: float = Field(..., ge=0, le=100, description="Credit utilization %")

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": "CUST-00001",
                "name": "Rajesh Kumar",
                "salary_delay_days": 5,
                "balance_trend": -10.5,
                "bill_payment_delay": 8,
                "transaction_anomaly": 2.1,
                "discretionary_drop_pct": 35.0,
                "atm_withdrawal_spike": 2.0,
                "failed_auto_debits": 1,
                "lending_app_txns": 3,
                "savings_drawdown_pct": 25.0,
                "credit_utilization": 65.0,
            }
        }


class FeatureContribution(BaseModel):
    """Single feature's contribution to prediction."""
    feature: str
    shap_value: Optional[float] = None
    importance: Optional[float] = None
    actual_value: float
    direction: Optional[str] = None


class PredictionResponse(BaseModel):
    """Model prediction result with explanation."""
    customer_id: Optional[str] = None
    prediction: int
    probability: float
    risk_level: str
    explanation: str
    top_features: List[FeatureContribution]
    shap_values: Optional[dict] = None


# ---- Customer ----

class CustomerCreate(BaseModel):
    """Schema for creating a customer record."""
    customer_id: str
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pan_number: Optional[str] = None
    aadhaar_masked: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    bank_branch: Optional[str] = None
    occupation: Optional[str] = None
    monthly_income_inr: int = 0
    loan_type: Optional[str] = None
    loan_amount_inr: int = 0
    emi_amount_inr: int = 0
    loan_tenure_months: int = 0
    active_loans: int = 1
    emi_to_income_ratio: float = 0
    upi_txn_count: int = 0
    salary_delay_days: float = 0
    balance_trend: float = 0
    bill_payment_delay: float = 0
    transaction_anomaly: float = 0
    discretionary_drop_pct: float = 0
    atm_withdrawal_spike: float = 1.0
    failed_auto_debits: int = 0
    lending_app_txns: int = 0
    savings_drawdown_pct: float = 0
    credit_utilization: float = 0


class CustomerResponse(BaseModel):
    """Schema for customer record response."""
    id: int
    customer_id: str
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pan_number: Optional[str] = None
    aadhaar_masked: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    bank_branch: Optional[str] = None
    occupation: Optional[str] = None
    monthly_income_inr: Optional[int] = 0
    loan_type: Optional[str] = None
    loan_amount_inr: Optional[int] = 0
    emi_amount_inr: Optional[int] = 0
    loan_tenure_months: Optional[int] = 0
    active_loans: Optional[int] = 1
    emi_to_income_ratio: Optional[float] = 0
    upi_txn_count: Optional[int] = 0
    salary_delay_days: float
    balance_trend: float
    bill_payment_delay: float
    transaction_anomaly: float
    discretionary_drop_pct: float
    atm_withdrawal_spike: float
    failed_auto_debits: int
    lending_app_txns: int
    savings_drawdown_pct: float
    credit_utilization: float
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---- Dashboard ----

class RiskDistribution(BaseModel):
    """Risk distribution summary for dashboard."""
    low: int
    medium: int
    high: int
    total: int


class DashboardStats(BaseModel):
    """Overall dashboard statistics."""
    total_customers: int
    total_predictions: int
    risk_distribution: RiskDistribution
    avg_risk_probability: float
    alerts_pending: int
