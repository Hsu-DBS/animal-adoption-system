# References:
# https://fastapi.tiangolo.com/tutorial/static-files/
# https://docs.python.org/3/library/pathlib.html


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
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


# Resolve the absolute path of the current file
BASE_DIR = Path(__file__).resolve().parent

# Define the directory where animal images are stored (server/app/src/images)
IMAGES_DIR = BASE_DIR / "src" / "images"

# Creates the directory if it does not exist
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Mount the images directory
app.mount(
    "/images",
    StaticFiles(directory=str(IMAGES_DIR)),
    name="images",
)

@app.get("/")
def read_root():
    return {
        "is_alive": True,
        "name": "Digital Animal Adoption System"
    }
