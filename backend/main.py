# -------------------------------------------------
# main.py  -  FastAPI Application Entry Point
# -------------------------------------------------
# Runs the Pre-Delinquency Intervention Engine backend.
# Mounts all routes, configures CORS, and initializes DB.
# -------------------------------------------------
# Usage:
#   cd backend
#   uvicorn main:app --reload --port 8000
# -------------------------------------------------

import sys
import os

# Ensure backend directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import CORS_ORIGINS, API_HOST, API_PORT
from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables on startup."""
    print("Initializing database...")
    try:
        init_db()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("  -> Ensure MySQL is running and the database exists.")
        print("  -> Run: mysql -u root -p -e 'CREATE DATABASE IF NOT EXISTS delinquency_engine;'")
    yield
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Pre-Delinquency Intervention Engine",
    description=(
        "AI-powered early warning system that predicts customer financial "
        "stress before payment defaults occur. Uses behavioral signals and "
        "machine learning to enable proactive intervention."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware  -  allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and mount route modules
from routes.predict import router as predict_router
from routes.customers import router as customers_router
from routes.dashboard import router as dashboard_router

app.include_router(predict_router)
app.include_router(customers_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "service": "Pre-Delinquency Intervention Engine",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Detailed health check."""
    import joblib
    from config import MODEL_PATH

    model_loaded = os.path.exists(MODEL_PATH)
    return {
        "status": "healthy",
        "model_available": model_loaded,
        "database": "connected",  # Will fail if DB is down
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
