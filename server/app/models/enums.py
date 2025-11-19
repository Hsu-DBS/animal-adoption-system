from enum import Enum


#Enum Reference: https://github.com/pydantic/pydantic/discussions/4967

class UserType(str, Enum):
    Admin = "Admin"
    Adopter = "Adopter"


class AdoptionStatus(str, Enum):
    Available = "Available"
    Adopted = "Adopted"


class ApplicationStatus(str, Enum):
    Submitted = "Submitted"
    Approved = "Approved"
    Rejected = "Rejected"