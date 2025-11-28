from pydantic import BaseModel
from typing import Optional
from app.models.enums import ApplicationStatus

class CreateApplicationRequest(BaseModel):
    animal_id: int
    reason: Optional[str] = None

class UpdateApplicationStatusRequest(BaseModel):
    application_status: ApplicationStatus