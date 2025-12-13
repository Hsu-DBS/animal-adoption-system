# References:
# https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
# https://fastapi.tiangolo.com/advanced/settings/


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Read database URL from environment variable
# Fallback to SQLite for local development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./digital_animal_adoption.db"
)

# SQLite needs check_same_thread, PostgreSQL does not
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# Create session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Provides a database session and ensures it is closed after the request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()