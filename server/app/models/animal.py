from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
from app.models.base_model import CommonBase
from app.models.enums import AdoptionStatus


class Animal(CommonBase):
    __tablename__ = "tbl_animals"

    name = Column(String(100), nullable=False)
    species = Column(String(50), nullable=False)
    breed = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=False)
    description = Column(Text, nullable=True)
    photo_url = Column(String, nullable=False)
    adoption_status = Column(Enum(AdoptionStatus), nullable=False, default=AdoptionStatus.Available)

    # Relationship
    applications = relationship("Application", back_populates="animal")
