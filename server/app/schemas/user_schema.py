from pydantic import BaseModel, EmailStr


class CreateAdminRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str | None = None
    address: str | None = None


class UpdateAdminRequest(CreateAdminRequest):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class CreateAdopterRequest(CreateAdminRequest):
    phone: str
    address: str