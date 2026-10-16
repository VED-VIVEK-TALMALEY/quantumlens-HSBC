"""Generate embeddings.json through the embedding microservice (no model in API process)."""
import json
from pathlib import Path
from supabase import create_client
from src.config.settings import settings
from src.rag.embedding_client import embed_texts
from src.utils.logger import logger


def build_embedding_text(record):
    period_values = record.get("period_values") or []
    values_text = "\n".join(
        f"{item.get('period_label') or ('Period ' + str(item.get('period_index', '?')))}: {item.get('value')}"
        for item in period_values if isinstance(item, dict)
    ) or "Not Available"

    return (
        f"Metric Name:\n{record.get('metric_name')}\n"
        f"Abbreviation:\n{record.get('abbreviation')}\n"
        f"Workbook:\n{record.get('source_workbook')}\n"
        f"Sheet:\n{record.get('sheet_name')}\n"
        f"Row Number:\n{record.get('row_number')}\n"
        f"Values:\n{values_text}"
    )


def _fetch_all_metrics(client):
    rows, start, page_size = [], 0, 1000
    while True:
        response = client.table("metrics").select("*").range(start, start + page_size - 1).execute()
        page = response.data or []
        rows.extend(page)
        if len(page) < page_size: break
        start += page_size
    return rows


def generate_embeddings(batch_size: int = 32):
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be configured")
    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    rows = _fetch_all_metrics(client)
    embeddings = []
    for start in range(0, len(rows), batch_size):
        batch = rows[start:start + batch_size]
        texts = [build_embedding_text(row) for row in batch]
        vectors = embed_texts(texts)
        for row, text, vector in zip(batch, texts, vectors):
            embeddings.append({
                "id": row.get("id"), "metric_id": row.get("metric_id"),
                "metric_name": row.get("metric_name"), "abbreviation": row.get("abbreviation"),
                "sheet_name": row.get("sheet_name"), "source_workbook": row.get("source_workbook"),
                "row_number": row.get("row_number"), "period_values": row.get("period_values") or [],
                "text": text, "embedding": vector,
            })
        logger.info("Embedded %s/%s records", min(start + len(batch), len(rows)), len(rows))
    settings.EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with settings.EMBEDDINGS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(embeddings, handle, indent=2, ensure_ascii=False)
    logger.info("Saved %s embeddings to %s", len(embeddings), settings.EMBEDDINGS_PATH)
    return embeddings

if __name__ == "__main__":
    generate_embeddings()
