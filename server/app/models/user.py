from sqlalchemy import Column, String, Enum
from app.models.base_model import BaseModel
from app.enums import UserType


class User(BaseModel):
    __tablename__ = "tbl_users"

    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)

    user_type = Column(Enum(UserType), nullable=False)
