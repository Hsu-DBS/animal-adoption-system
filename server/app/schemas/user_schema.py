from pydantic import BaseModel, EmailStr

class CreateAdminRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str | None = None
    address: str | None = None