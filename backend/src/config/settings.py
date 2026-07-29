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

    VECTOR_DB_PATH = Path(
        os.getenv(
            "VECTOR_DB_PATH",
            str(VECTOR_DB_DIR)
        )
    )

    EMBEDDINGS_PATH = GENERATED_DATA_DIR / "embeddings.json"

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    LLM_MODEL = "llama-3.3-70b-versatile"

    TEMPERATURE = 0.2
    MAX_TOKENS = 512

    TOP_K = 5

    ORACLE_USER = os.getenv("ORACLE_USER")
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")

    ORACLE_HOST = os.getenv(
        "ORACLE_HOST",
        "localhost"
    )

    ORACLE_PORT = int(
        os.getenv(
            "ORACLE_PORT",
            "1521"
        )
    )

    ORACLE_SERVICE = os.getenv(
        "ORACLE_SERVICE",
        "XEPDB1"
    )

    ORACLE_DSN = os.getenv(
        "ORACLE_DSN",
        f"{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"
    )


for directory in [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    GENERATED_DATA_DIR,
    VECTOR_DB_DIR,
    LOG_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)


settings = Settings()


if __name__ == "__main__":

    print("BASE_DIR       :", settings.BASE_DIR)
    print("DATA_DIR       :", settings.DATA_DIR)
    print("VECTOR_DB_PATH :", settings.VECTOR_DB_PATH)
    print("ORACLE_DSN     :", settings.ORACLE_DSN)