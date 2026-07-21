from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from src.core.exceptions import register_exception_handlers
from src.api.routes import router
from src.api.middleware import RequestLoggingMiddleware

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

app.include_router(router)
register_exception_handlers(app)

@app.get("/")
def root():
    return {
        "project": "QuantumLens",
        "status": "Running",
    }