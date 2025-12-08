from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db.database import Base, engine
from app.endpoints import (
    auth_router,
    user_router,
    animal_router,
    application_router,
    dashboard_router,
)


app = FastAPI()

# Create all tables on startup
Base.metadata.create_all(bind=engine)

# CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(animal_router)
app.include_router(application_router)
app.include_router(dashboard_router)

# Mount a static file directory so FastAPI can serve animal images
app.mount(
    "/images",                                # Public URL prefix, frontend accesses images at /images/<filename>
    StaticFiles(directory="app/src/images"),  # Physical directory where uploaded images are stored in the backend
    name="images"                             # Optional name for route identification
)


@app.get("/")
def read_root():
    return {
        "is_alive": True,
        "name": "Digital Animal Adoption System"
    }
