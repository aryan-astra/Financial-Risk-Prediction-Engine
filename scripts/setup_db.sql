-- =====================================================
-- Pre-Delinquency Intervention Engine  -  Database Setup
-- =====================================================
-- Run this script to initialize the MySQL database.
-- Usage: mysql -u root -p < scripts/setup_db.sql
-- =====================================================

-- Create database
CREATE DATABASE IF NOT EXISTS delinquency_engine
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE delinquency_engine;

-- Customers table: stores Indian customer financial signal snapshots
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    phone VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    pan_number VARCHAR(15),
    aadhaar_masked VARCHAR(20),
    account_number VARCHAR(20),
    ifsc_code VARCHAR(15),
    bank_branch VARCHAR(50),
    occupation VARCHAR(50),
    monthly_income_inr INT DEFAULT 0,
    loan_type VARCHAR(30),
    loan_amount_inr INT DEFAULT 0,
    emi_amount_inr INT DEFAULT 0,
    loan_tenure_months INT DEFAULT 0,
    active_loans INT DEFAULT 1,
    emi_to_income_ratio FLOAT DEFAULT 0,
    upi_txn_count INT DEFAULT 0,

    -- Financial stress signals (core ML features)
    salary_delay_days FLOAT DEFAULT 0,
    balance_trend FLOAT DEFAULT 0,
    bill_payment_delay FLOAT DEFAULT 0,
    transaction_anomaly FLOAT DEFAULT 0,
    discretionary_drop_pct FLOAT DEFAULT 0,
    atm_withdrawal_spike FLOAT DEFAULT 1.0,
    failed_auto_debits INT DEFAULT 0,
    lending_app_txns INT DEFAULT 0,
    savings_drawdown_pct FLOAT DEFAULT 0,
    credit_utilization FLOAT DEFAULT 0,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_customer_id (customer_id)
) ENGINE=InnoDB;

-- Prediction results table: stores ML model outputs
CREATE TABLE IF NOT EXISTS prediction_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,

    -- Model outputs
    risk_probability FLOAT NOT NULL,
    risk_level VARCHAR(10) NOT NULL,
    prediction INT NOT NULL,

    -- Explanation
    explanation TEXT,
    top_features_json TEXT,

    -- Alert tracking
    alert_sent BOOLEAN DEFAULT FALSE,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_pred_customer (customer_id),
    INDEX idx_pred_risk_level (risk_level),
    INDEX idx_pred_created (created_at)
) ENGINE=InnoDB;

-- Insert sample Indian customers for demo purposes
INSERT IGNORE INTO customers (customer_id, name, gender, age, phone, city, state, pan_number, aadhaar_masked, account_number, ifsc_code, bank_branch, occupation, monthly_income_inr, loan_type, loan_amount_inr, emi_amount_inr, loan_tenure_months, active_loans, emi_to_income_ratio, upi_txn_count, salary_delay_days, balance_trend, bill_payment_delay, transaction_anomaly, discretionary_drop_pct, atm_withdrawal_spike, failed_auto_debits, lending_app_txns, savings_drawdown_pct, credit_utilization)
VALUES
    ('CUST-000001', 'Rajesh Kumar', 'Male', 34, '+91-9876543210', 'Mumbai', 'Maharashtra', 'ABCDE1234F', 'XXXX-XXXX-5678', '100145678901', 'SBIN0001234', 'SBI Main Branch', 'Software Engineer', 85000, 'Home Loan', 4500000, 37500, 120, 2, 44.12, 52, 2, -3.5, 3, 0.8, 10, 1.1, 0, 1, 5, 30),
    ('CUST-000002', 'Priya Sharma', 'Female', 29, '+91-9123456789', 'Delhi', 'Delhi', 'FGHIJ5678K', 'XXXX-XXXX-1234', '200423456789', 'HDFC0005678', 'HDFC Bank', 'Marketing Manager', 65000, 'Personal Loan', 800000, 22222, 36, 3, 34.19, 78, 12, -25.0, 18, 3.2, 55, 2.8, 3, 7, 60, 82),
    ('CUST-000003', 'Amit Singh', 'Male', 42, '+91-8765432109', 'Bengaluru', 'Karnataka', 'KLMNO9012P', 'XXXX-XXXX-9012', '305612345678', 'ICIC0009012', 'ICICI Bank', 'Business Owner', 150000, 'Business Loan', 2500000, 41667, 60, 1, 27.78, 35, 0, 5.0, 1, 0.2, 3, 0.7, 0, 0, 2, 15),
    ('CUST-000004', 'Neha Patel', 'Female', 31, '+91-7654321098', 'Ahmedabad', 'Gujarat', 'PQRST3456U', 'XXXX-XXXX-3456', '500198765432', 'UTIB0003456', 'Axis Bank', 'CA/Accountant', 95000, 'Car Loan', 1200000, 25000, 48, 2, 26.32, 45, 8, -15.0, 10, 1.8, 35, 2.0, 1, 4, 30, 55),
    ('CUST-000005', 'Vikram Reddy', 'Male', 38, '+91-6543210987', 'Hyderabad', 'Telangana', 'UVWXY7890Z', 'XXXX-XXXX-7890', '623412345678', 'BARB0007890', 'Bank of Baroda', 'Driver', 25000, 'Two Wheeler Loan', 150000, 6250, 24, 4, 25.00, 15, 20, -40.0, 25, 4.5, 75, 4.0, 5, 12, 85, 95),
    ('CUST-000006', 'Sunita Joshi', 'Female', 45, '+91-9988776655', 'Pune', 'Maharashtra', 'DEFGH2345I', 'XXXX-XXXX-2345', '100167890123', 'SBIN0002345', 'SBI Main Branch', 'Teacher', 45000, 'Gold Loan', 300000, 12500, 24, 1, 27.78, 28, 5, -8.0, 7, 1.2, 20, 1.5, 1, 2, 15, 40),
    ('CUST-000007', 'Karan Malhotra', 'Male', 27, '+91-8877665544', 'Gurugram', 'Haryana', 'JKLMN6789O', 'XXXX-XXXX-6789', '200478901234', 'HDFC0001111', 'HDFC Bank', 'Sales Executive', 55000, 'Credit Card EMI', 200000, 16667, 12, 2, 30.30, 92, 15, -28.0, 20, 2.8, 48, 3.2, 4, 9, 55, 78),
    ('CUST-000008', 'Meera Iyer', 'Female', 52, '+91-7766554433', 'Chennai', 'Tamil Nadu', 'NOPQR0123S', 'XXXX-XXXX-0123', '305689012345', 'CNRB0002222', 'Canara Bank', 'Government Employee', 72000, 'Home Loan', 3500000, 19444, 180, 1, 27.01, 18, 1, 2.0, 2, 0.5, 8, 0.9, 0, 0, 4, 22),
    ('CUST-000009', 'Farhan Ahmed', 'Male', 36, '+91-6655443322', 'Lucknow', 'Uttar Pradesh', 'RSTUV4567W', 'XXXX-XXXX-4567', '500134567890', 'PUNB0003333', 'Punjab National Bank', 'Shopkeeper', 35000, 'Personal Loan', 500000, 13889, 36, 3, 39.68, 42, 10, -18.0, 14, 2.1, 42, 2.4, 2, 5, 38, 65),
    ('CUST-000010', 'Ananya Banerjee', 'Female', 24, '+91-9345678901', 'Kolkata', 'West Bengal', 'WXYZA8901B', 'XXXX-XXXX-8901', '623456789012', 'UBIN0004444', 'Union Bank of India', 'Freelancer', 40000, 'Education Loan', 600000, 10000, 60, 1, 25.00, 65, 3, -5.0, 5, 1.0, 15, 1.2, 0, 1, 10, 35);

SELECT 'Database setup complete!' AS status;
