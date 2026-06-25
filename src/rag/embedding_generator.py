from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from supabase import create_client
import os
import json

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# -----------------------------
# Load Embedding Model
# -----------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------
# Build Text for Embedding
# -----------------------------

def build_embedding_text(record):

    return f"""
Metric Name: {record.get('metric_name')}
Abbreviation: {record.get('abbreviation')}
Workbook: {record.get('source_workbook')}
Sheet: {record.get('sheet_name')}
"""

# -----------------------------
# Generate Embeddings
# -----------------------------

def generate_embeddings():

    rows = (
        supabase
        .table("metrics")
        .select("*")
        .execute()
        .data
    )

    print(f"Fetched {len(rows)} KPI records")

    embeddings = []

    for row in rows:

        text = build_embedding_text(row)

        vector = model.encode(
            text
        ).tolist()

        embeddings.append({
            "metric_id": row.get("metric_id"),
            "metric_name": row.get("metric_name"),
            "abbreviation": row.get("abbreviation"),
            "sheet_name": row.get("sheet_name"),
            "source_workbook": row.get("source_workbook"),
            "text": text,
            "embedding": vector
        })

    return embeddings

# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    vectors = generate_embeddings()

    with open(
        "embeddings.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            vectors,
            f,
            indent=2
        )

    print(
        f"Generated {len(vectors)} embeddings"
    )

    print(
        "Saved embeddings.json"
    )