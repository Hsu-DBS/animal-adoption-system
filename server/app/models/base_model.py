from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base
from datetime import datetime


class CommonBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=True, default=None)
    updated_by = Column(String, nullable=True)
