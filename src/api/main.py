from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="QuantumLens API",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():

    return {
        "project": "QuantumLens",
        "status": "Running"
    }