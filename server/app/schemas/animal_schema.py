from pydantic import BaseModel
from app.models.enums import AdoptionStatus

class CreateAnimalRequest(BaseModel):
    name: str
    species: str
    breed: str
    age: int | None = None
    gender: str
    description: str | None = None
    adoption_status: AdoptionStatus = AdoptionStatus.Available
