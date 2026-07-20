from dotenv import load_dotenv

import os
from pathlib import Path

load_dotenv()

# ==========================================================
# Base Directories
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

GENERATED_DATA_DIR = DATA_DIR / "generated"

VECTOR_DB_DIR = DATA_DIR / "vectordb"

LOG_DIR = BASE_DIR / "logs"

# ==========================================================
# Settings
# ==========================================================


class Settings:

    # ------------------------------------------------------
    # Data Paths
    # ------------------------------------------------------

    BASE_DIR = BASE_DIR

    DATA_DIR = DATA_DIR

    RAW_DATA_DIR = RAW_DATA_DIR

    PROCESSED_DATA_DIR = PROCESSED_DATA_DIR

    GENERATED_DATA_DIR = GENERATED_DATA_DIR

    VECTOR_DB_PATH = Path(
        os.getenv(
            "VECTOR_DB_PATH",
            str(VECTOR_DB_DIR)
        )
    )

    EMBEDDINGS_PATH = (
        GENERATED_DATA_DIR / "embeddings.json"
    )

    # ------------------------------------------------------
    # Supabase
    # ------------------------------------------------------

    SUPABASE_URL = os.getenv("SUPABASE_URL")

    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # ------------------------------------------------------
    # Groq
    # ------------------------------------------------------

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # ------------------------------------------------------
    # Embedding Model
    # ------------------------------------------------------

    EMBEDDING_MODEL = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # ------------------------------------------------------
    # LLM
    # ------------------------------------------------------

    LLM_MODEL = (
        "llama-3.3-70b-versatile"
    )

    TEMPERATURE = 0.2

    MAX_TOKENS = 512

    # ------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------

    TOP_K = 5


settings = Settings()

