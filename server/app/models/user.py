from sqlalchemy import Column, String, Enum, Boolean
from app.models.base_model import CommonBase
from sqlalchemy.orm import relationship
from app.models.enums import UserType


class User(CommonBase):
    __tablename__ = "tbl_users"

    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)

    user_type = Column(Enum(UserType), nullable=False)

    # Relationship
    applications = relationship("Application", back_populates="adopter")
