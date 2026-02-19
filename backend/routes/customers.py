# -------------------------------------------------
# routes/customers.py  -  Customer Data Endpoints
# -------------------------------------------------
# CRUD endpoints for customer records and data
# ingestion into the MySQL database.
# -------------------------------------------------

import sys
import os
import csv
import io
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_db
from models import Customer
from schemas import CustomerCreate, CustomerResponse

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("/", response_model=List[CustomerResponse])
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """List all customers with pagination."""
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """Retrieve a single customer by ID."""
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/", response_model=CustomerResponse)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    """Create or update a customer record."""
    existing = db.query(Customer).filter(Customer.customer_id == data.customer_id).first()

    if existing:
        # Update existing customer
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing

    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.post("/bulk-ingest")
def bulk_ingest(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Bulk ingest customer data from a CSV file.
    Expects columns matching the customer signal features.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))

    created = 0
    updated = 0
    errors = []

    for i, row in enumerate(reader):
        try:
            customer_id = row.get("customer_id", f"BULK-{i+1:05d}")
            existing = db.query(Customer).filter(
                Customer.customer_id == customer_id
            ).first()

            fields = {
                "customer_id": customer_id,
                "name": row.get("name"),
                "gender": row.get("gender"),
                "age": int(row["age"]) if row.get("age") else None,
                "phone": row.get("phone"),
                "city": row.get("city"),
                "state": row.get("state"),
                "pan_number": row.get("pan_number"),
                "aadhaar_masked": row.get("aadhaar_masked"),
                "account_number": row.get("account_number"),
                "ifsc_code": row.get("ifsc_code"),
                "bank_branch": row.get("bank_branch"),
                "occupation": row.get("occupation"),
                "monthly_income_inr": int(row.get("monthly_income_inr", 0)),
                "loan_type": row.get("loan_type"),
                "loan_amount_inr": int(row.get("loan_amount_inr", 0)),
                "emi_amount_inr": int(row.get("emi_amount_inr", 0)),
                "loan_tenure_months": int(row.get("loan_tenure_months", 0)),
                "active_loans": int(row.get("active_loans", 1)),
                "emi_to_income_ratio": float(row.get("emi_to_income_ratio", 0)),
                "upi_txn_count": int(row.get("upi_txn_count", 0)),
                "salary_delay_days": float(row.get("salary_delay_days", 0)),
                "balance_trend": float(row.get("balance_trend", 0)),
                "bill_payment_delay": float(row.get("bill_payment_delay", 0)),
                "transaction_anomaly": float(row.get("transaction_anomaly", 0)),
                "discretionary_drop_pct": float(row.get("discretionary_drop_pct", 0)),
                "atm_withdrawal_spike": float(row.get("atm_withdrawal_spike", 1.0)),
                "failed_auto_debits": int(row.get("failed_auto_debits", 0)),
                "lending_app_txns": int(row.get("lending_app_txns", 0)),
                "savings_drawdown_pct": float(row.get("savings_drawdown_pct", 0)),
                "credit_utilization": float(row.get("credit_utilization", 0)),
            }

            if existing:
                for key, value in fields.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                db.add(Customer(**fields))
                created += 1
        except Exception as e:
            errors.append({"row": i + 1, "error": str(e)})

    db.commit()

    return {
        "created": created,
        "updated": updated,
        "errors": errors,
        "total_processed": created + updated + len(errors),
    }


@router.delete("/{customer_id}")
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    """Delete a customer record."""
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": f"Customer {customer_id} deleted"}
