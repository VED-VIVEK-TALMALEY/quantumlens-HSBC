"""Runtime settings for the Supabase-based QuantumLens backend."""
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
GENERATED_DATA_DIR = DATA_DIR / "generated"
VECTOR_DB_DIR = DATA_DIR / "vectordb"
LOG_DIR = BASE_DIR / "logs"

class Settings:
    BASE_DIR = BASE_DIR
    DATA_DIR = DATA_DIR
    RAW_DATA_DIR = RAW_DATA_DIR
    PROCESSED_DATA_DIR = PROCESSED_DATA_DIR
    GENERATED_DATA_DIR = GENERATED_DATA_DIR
    VECTOR_DB_PATH = Path(os.getenv("VECTOR_DB_PATH", str(VECTOR_DB_DIR)))
    EMBEDDINGS_PATH = GENERATED_DATA_DIR / "embeddings.json"
    SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    # Keep this model identical to the model used to build the existing Chroma collection.
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    EMBEDDING_SERVICE_URL = os.getenv("EMBEDDING_SERVICE_URL", "http://127.0.0.1:8001").rstrip("/")
    EMBEDDING_SERVICE_TIMEOUT = float(os.getenv("EMBEDDING_SERVICE_TIMEOUT", "90"))
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "512"))
    TOP_K = int(os.getenv("TOP_K", "5"))

for directory in (DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, GENERATED_DATA_DIR, VECTOR_DB_DIR, LOG_DIR):
    directory.mkdir(parents=True, exist_ok=True)
settings = Settings()
