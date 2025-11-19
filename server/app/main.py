from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "is_alive": True,
        "name": "Digital Animal Adoption System"
    }
