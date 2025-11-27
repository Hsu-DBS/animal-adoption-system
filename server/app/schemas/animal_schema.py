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


class UpdateAnimalRequest(CreateAnimalRequest):
    name: str | None = None
    species: str | None = None
    breed: str | None = None
    gender: str | None = None
    adoption_status: AdoptionStatus | None = None