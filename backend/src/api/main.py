# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.api.middleware import RequestLoggingMiddleware
from src.api.exceptions import register_exception_handlers

from src.api.routers.health import router as health_router
from src.api.routers.metrics import router as metrics_router
from src.api.routers.rag import router as rag_router
from src.api.routers.records import router as records_router
from src.api.routers.query import router as query_router
from src.api.routers.agent import router as agent_router

app = FastAPI(
    title="QuantumLens API",
    version="1.0.0",
)

app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1024,
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

register_exception_handlers(app)

app.include_router(health_router)
app.include_router(metrics_router)
app.include_router(rag_router)
app.include_router(records_router)
app.include_router(query_router)
app.include_router(agent_router)

@app.get("/")
def root():
    return {
        "project": "QuantumLens",
        "status": "Running",
    }