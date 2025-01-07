"""Database module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

from .core.config import settings

# Create base class for models
Base = declarative_base()

# Create database engine
engine = create_engine(
    settings.get_database_url(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """Initialize database"""
    # Import models here to avoid circular imports
    from .db.base import Base  # noqa: F811
    Base.metadata.create_all(bind=engine)