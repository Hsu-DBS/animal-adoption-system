from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import auth_router

app = FastAPI()

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

@app.get("/")
def read_root():
    return {
        "is_alive": True,
        "name": "Digital Animal Adoption System"
    }
