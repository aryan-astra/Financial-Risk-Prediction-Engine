# -------------------------------------------------
# preprocess.py  -  Data Preprocessing Utilities
# -------------------------------------------------
# Functions for loading, cleaning, splitting, and scaling
# the customer financial signals dataset.
# -------------------------------------------------

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Feature columns used by the model
FEATURE_COLUMNS = [
    "salary_delay_days",
    "balance_trend",
    "bill_payment_delay",
    "transaction_anomaly",
    "discretionary_drop_pct",
    "atm_withdrawal_spike",
    "failed_auto_debits",
    "lending_app_txns",
    "savings_drawdown_pct",
    "credit_utilization",
]

TARGET_COLUMN = "default"

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "customer_signals.csv")


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Load dataset from CSV. Generate if not found."""
    if not os.path.exists(path):
        print("Dataset not found. Generating synthetic data...")
        from generate_data import generate_dataset, OUTPUT_PATH
        df = generate_dataset()
        df.to_csv(OUTPUT_PATH, index=False)
        return df
    return pd.read_csv(path)


def preprocess(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """
    Preprocess the dataframe:
      1. Select feature and target columns
      2. Handle missing values (fill with median)
      3. Train/test split
      4. Standard scaling

    Returns:
        X_train, X_test, y_train, y_test, scaler, feature_names
    """
    # Select columns
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    # Fill missing values with column median
    X = X.fillna(X.median())

    # Train/test split (stratified to preserve class balance)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Standard scaling (fit on train, transform both)
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=FEATURE_COLUMNS,
        index=X_train.index,
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=FEATURE_COLUMNS,
        index=X_test.index,
    )

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, FEATURE_COLUMNS


if __name__ == "__main__":
    df = load_data()
    X_train, X_test, y_train, y_test, scaler, features = preprocess(df)
    print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")
    print(f"Train default rate: {y_train.mean():.2%}")
    print(f"Test default rate:  {y_test.mean():.2%}")
