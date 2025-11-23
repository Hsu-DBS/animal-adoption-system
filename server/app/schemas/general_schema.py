from pydantic import BaseModel
from typing import Optional, Dict, Any


class GeneralResponse(BaseModel):
    message: str
    data: Optional[Dict[str, Any]] = None
