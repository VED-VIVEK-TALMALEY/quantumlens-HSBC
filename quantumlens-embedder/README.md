# QuantumLens Embedder

Embedding microservice for QuantumLens.

## Model

BAAI/bge-small-en-v1.5

## Run

```bash
pip install -r requirements.txt

uvicorn app:app --reload
```

## Endpoints

GET /

GET /health

POST /embed

Example request

```json
{
    "texts":[
        "Revenue",
        "Net Interest Income"
    ]
}
```

Example response

```json
{
    "embeddings":[
        [...],
        [...]
    ]
}
```