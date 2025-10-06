"""
Database connection and session management

This module handles the SQLAlchemy database engine, session factory,
and provides utilities for database operations with PostgreSQL and PostGIS.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create SQLAlchemy engine
# The echo=True parameter will log all SQL statements (useful for debugging)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=300      # Recycle connections every 5 minutes
)

# Create SessionLocal class - this will be our database session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for our SQLAlchemy models
# All our database models will inherit from this Base class
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session
    
    This is a generator function that creates a database session,
    yields it to the calling function, and then closes it automatically.
    This ensures proper session management and prevents connection leaks.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables
    
    This function should be called once when the application starts
    to ensure all tables are created. In production, you might want
    to use Alembic migrations instead.
    """
    # Import all models here to ensure they are registered with Base
    from app.models import bus_stop  # noqa
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
