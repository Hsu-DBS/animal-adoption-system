# References:
# https://noplacelikelocalhost.medium.com/testing-crud-operations-with-sqlite-a-time-saving-guide-for-developers-7c74405d63d5
# Dependencies & Overrides: https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-the-app-dependency-overrides-attribute
# SQLite: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#threading-pooling-behavior
# Pytest - Fixtures: https://docs.pytest.org/en/stable/how-to/fixtures.html
# Pytest - Fixture scopes: https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-scopes


import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, get_db
from app.models.enums import UserType
from app.models.user import User
from app.utils.auth_util import hash_password


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


# common function to create users
def create_test_user(name, email, phone, address, password, role):

    user = User(
        name=name,
        email=email,
        phone=phone,
        address=address,
        password=hash_password(password),
        user_type=role,
        is_deleted=False,
        created_at=datetime.utcnow(),
        created_by="system",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {
        "id": user.id,
    }


# create default admin account
@pytest.fixture(scope="session")
def test_admin():
    return create_test_user(
        name="Admin",
        email="admin@gmail.com",
        phone="0912345678",
        address="Dublin",
        password="Admin@123",
        role=UserType.Admin.value,
    )


# create default adopter account
@pytest.fixture(scope="session")
def test_adopter():
    return create_test_user(
        name="Adopter",
        email="adopter@gmail.com",
        phone="0998765432",
        address="Dublin",
        password="Adopter@123",
        role=UserType.Adopter.value,
    )
