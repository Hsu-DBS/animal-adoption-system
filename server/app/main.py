from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.endpoints import (
    auth_router,
    user_router
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

@app.get("/")
def read_root():
    return {
        "is_alive": True,
        "name": "Digital Animal Adoption System"
    }
