from pydantic import BaseModel
from typing import Optional

class CreateApplicationRequest(BaseModel):
    animal_id: int
    reason: Optional[str] = None
