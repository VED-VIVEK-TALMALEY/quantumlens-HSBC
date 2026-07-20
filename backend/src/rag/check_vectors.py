import chromadb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

client = chromadb.PersistentClient(
    path=str(BASE_DIR / "vector_db")
)

collection = client.get_or_create_collection(
    name="hsbc_kpis"
)

print(
    "Vector Count:",
    collection.count()
)   