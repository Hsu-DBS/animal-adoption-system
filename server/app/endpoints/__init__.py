from app.endpoints.auth_management import router as auth_router
from app.endpoints.user_management import router as user_router
from app.endpoints.animal_management import router as animal_router

__all__ = [
    "auth_router",
    "user_router",
    "animal_router",
]