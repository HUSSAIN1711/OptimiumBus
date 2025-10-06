"""
Database initialization script for OptimumBus

This script initializes the database with tables and spatial indexes.
Run this script after setting up PostgreSQL and PostGIS.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine, Base, init_db
from app.core.geospatial_utils import create_spatial_indexes
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Initialize the database with tables and indexes"""
    try:
        logger.info("Initializing OptimumBus database...")
        
        # Create all tables
        logger.info("Creating database tables...")
        init_db()
        logger.info("✅ Database tables created successfully")
        
        # Create spatial indexes
        logger.info("Creating spatial indexes...")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            if create_spatial_indexes(db):
                logger.info("✅ Spatial indexes created successfully")
            else:
                logger.warning("⚠️ Failed to create spatial indexes")
        finally:
            db.close()
        
        logger.info("🎉 Database initialization completed successfully!")
        logger.info("You can now start the FastAPI server with: python run.py")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
