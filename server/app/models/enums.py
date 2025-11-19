from enum import Enum


#Enum Reference: https://github.com/pydantic/pydantic/discussions/4967

class UserType(str, Enum):
    admin = "admin"
    adopter = "adopter"
