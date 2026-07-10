from fastapi import FastAPI
from src.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

from src.api.services import (
    ask_question,
    search_metrics,
    get_all_metrics,
    get_metric_by_id
)
app = FastAPI(
    title="QuantumLens API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://quantumlens-hsbc.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():

    return {
        "project": "QuantumLens",
        "status": "Running"
    }