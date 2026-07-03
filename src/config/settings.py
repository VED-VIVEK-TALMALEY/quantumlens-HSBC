from dotenv import load_dotenv

import os
from pathlib import Path    
load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings:

    # ==========================
    # Supabase
    # ==========================

    SUPABASE_URL = os.getenv(
        "SUPABASE_URL"
    )

    SUPABASE_KEY = os.getenv(
        "SUPABASE_KEY"
    )

    # ==========================
    # Groq
    # ==========================

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )

    # ==========================
    # Embeddings
    # ==========================

    EMBEDDING_MODEL = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # ==========================
    # LLM
    # ==========================

    LLM_MODEL = (
        "llama-3.3-70b-versatile"
    )

    TEMPERATURE = 0.2

    MAX_TOKENS = 512

    # ==========================
    # Retrieval
    # ==========================

    TOP_K = 5
    VECTOR_DB_PATH = BASE_DIR / "src" / "rag" / "vector_db"
    EMBEDDINGS_PATH = BASE_DIR / "src" / "rag" / "embeddings.json"

settings = Settings()