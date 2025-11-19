from sqlalchemy import Column, ForeignKey, Integer, Text, Enum
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
from server.app.models.enums import ApplicationStatus


class Application(BaseModel):
    __tablename__ = "tbl_applications"

    animal_id = Column(Integer, ForeignKey("tbl_animals.id"), nullable=False)
    adopter_id = Column(Integer, ForeignKey("tbl_users.id"), nullable=False)

    application_status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.Submitted)
    reason = Column(Text, nullable=True)

    # Relationships
    animal = relationship("Animal", back_populates="applications")
    adopter = relationship("User", back_populates="applications")
