# -------------------------------------------------
# database.py  -  SQLAlchemy Database Setup
# -------------------------------------------------
# Configures the MySQL database engine, session, and
# base model class for the Pre-Delinquency Engine.
# -------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=False,         # Set True for SQL debug logging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.
    Automatically closes the session when done.
    Usage in FastAPI:  db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables defined in models.py."""
    import models  # noqa: F401  -  ensures models are registered
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
