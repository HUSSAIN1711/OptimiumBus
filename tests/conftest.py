import os
import typing as t
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the app and database/session utilities
from app.db.database import Base, get_db
from app.core.config import settings
from main import app

# IMPORTANT: Use a separate test database URL
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    settings.DATABASE_URL.replace("optimumbus_db", "optimumbus_db_test")
)

# Create a dedicated SQLAlchemy engine and session factory for tests
engine_test = create_engine(
    TEST_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create all tables in the test database at the start of the test session,
    and drop them when the session ends. This ensures isolation from dev DB.
    """
    # Create tables
    Base.metadata.create_all(bind=engine_test)
    yield
    # Drop tables after the entire test session
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def db_session():
    """Provide a SQLAlchemy session bound to the test database."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    """
    Provide a TestClient that uses the test database session by overriding
    the application's get_db dependency.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Clean up override after test
    app.dependency_overrides.pop(get_db, None)
