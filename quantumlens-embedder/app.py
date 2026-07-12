from fastapi import FastAPI, HTTPException

from embedding_service import EmbeddingService
from models import EmbeddingRequest, EmbeddingResponse
from config import MODEL_NAME, DEVICE

app = FastAPI(
    title="QuantumLens Embedding Service",
    version="1.0.0",
    description="Embedding microservice for QuantumLens"
)

# Load the model once when the application starts
embedding_service = EmbeddingService()


@app.get("/")
def root():
    return {
        "service": "QuantumLens Embedder",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "device": DEVICE
    }


@app.post("/embed", response_model=EmbeddingResponse)
def embed(request: EmbeddingRequest):
    try:
        embeddings = embedding_service.embed(request.texts)

        return EmbeddingResponse(
            embeddings=embeddings
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )