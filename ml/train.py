# -------------------------------------------------
# train.py  -  Model Training Script
# -------------------------------------------------
# Trains a RandomForestClassifier on customer financial
# signals to predict payment default risk. Evaluates model
# performance and saves the trained model + scaler.
# -------------------------------------------------
# Usage:
#   cd ml
#   python train.py
# -------------------------------------------------

import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)

# Local imports
from preprocess import load_data, preprocess, FEATURE_COLUMNS
from generate_data import generate_dataset, OUTPUT_PATH as DATA_OUTPUT

# Paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "risk_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.pkl")


def train_model():
    """Train the RandomForest model and evaluate performance."""

    # ---- Step 1: Load or generate data ----
    print("=" * 60)
    print("  Pre-Delinquency Intervention Engine  -  Model Training")
    print("=" * 60)

    data_path = os.path.join(os.path.dirname(__file__), "data", "customer_signals.csv")
    if not os.path.exists(data_path):
        print("\n[1/5] Generating synthetic dataset...")
        df = generate_dataset()
        df.to_csv(DATA_OUTPUT, index=False)
    else:
        print("\n[1/5] Loading existing dataset...")
        df = load_data(data_path)

    print(f"  -> {len(df)} samples, default rate: {df['default'].mean():.2%}")

    # ---- Step 2: Preprocess ----
    print("\n[2/5] Preprocessing data...")
    X_train, X_test, y_train, y_test, scaler, features = preprocess(df)
    print(f"  -> Train: {X_train.shape[0]} samples | Test: {X_test.shape[0]} samples")

    # ---- Step 3: Train model ----
    print("\n[3/5] Training RandomForestClassifier...")
    model = RandomForestClassifier(
        n_estimators=200,          # Number of trees
        max_depth=12,              # Limit depth to prevent overfitting
        min_samples_split=10,      # Minimum samples to split a node
        min_samples_leaf=5,        # Minimum samples in leaf node
        class_weight="balanced",   # Handle class imbalance
        random_state=42,
        n_jobs=-1,                 # Use all CPU cores
    )
    model.fit(X_train, y_train)
    print("  -> Training complete.")

    # ---- Step 4: Evaluate ----
    print("\n[4/5] Evaluating model performance...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)

    print(f"\n  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print(f"  ROC AUC:   {auc:.4f}")

    print(f"\n  Classification Report:\n")
    print(classification_report(y_test, y_pred, target_names=["No Default", "Default"]))

    print(f"  Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"    {cm}")

    # Feature importance
    importances = model.feature_importances_
    feat_imp = sorted(zip(features, importances), key=lambda x: x[1], reverse=True)
    print(f"\n  Feature Importances:")
    for fname, imp in feat_imp:
        bar = "#" * int(imp * 50)
        print(f"    {fname:<28s} {imp:.4f} {bar}")

    # ---- Step 5: Save model artifacts ----
    print("\n[5/5] Saving model artifacts...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(
        {
            "features": features,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "auc": auc,
            "n_estimators": model.n_estimators,
            "max_depth": model.max_depth,
        },
        METADATA_PATH,
    )
    print(f"  -> Model saved to {MODEL_PATH}")
    print(f"  -> Scaler saved to {SCALER_PATH}")
    print(f"  -> Metadata saved to {METADATA_PATH}")

    print("\n" + "=" * 60)
    print("  Training complete! Model is ready for serving.")
    print("=" * 60)

    return model, scaler


if __name__ == "__main__":
    train_model()
