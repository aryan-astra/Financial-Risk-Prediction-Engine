# -------------------------------------------------
# config.py  -  Backend Configuration
# -------------------------------------------------
# Loads settings from environment variables with defaults
# suitable for local development.
# -------------------------------------------------

import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file if present

# MySQL connection
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "delinquency_engine")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Model paths (relative to project root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, "ml", "models", "risk_model.pkl")
SCALER_PATH = os.path.join(PROJECT_ROOT, "ml", "models", "scaler.pkl")
METADATA_PATH = os.path.join(PROJECT_ROOT, "ml", "models", "model_metadata.pkl")

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
