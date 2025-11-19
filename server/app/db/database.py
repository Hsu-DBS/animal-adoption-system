from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Database SQLite URL
DATABASE_URL = "sqlite:///./digital_animal_adoption.db"

#Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

#Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base class for models
Base = declarative_base()
