# References:
# https://noplacelikelocalhost.medium.com/testing-crud-operations-with-sqlite-a-time-saving-guide-for-developers-7c74405d63d5
# Dependencies & Overrides: https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-the-app-dependency-overrides-attribute
# SQLite: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#threading-pooling-behavior
# Pytest - Fixtures: https://docs.pytest.org/en/stable/how-to/fixtures.html

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, get_db


# test database url
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# create db engine
# check_same_thread=False is required for SQLite because FastAPI uses multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# create a db session
# this will be used instead of the real database
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# override get_db dependency
# use the test database instead of the real database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# tell FastAPI to use override_get_db during tests
app.dependency_overrides[get_db] = override_get_db


# create & drops tables for testing
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Fastapi test client
# used to send requests to the API in tests
@pytest.fixture()
def client():
    return TestClient(app)
