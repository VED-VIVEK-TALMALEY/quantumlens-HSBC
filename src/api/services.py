from src.utils.logger import logger
from supabase import create_client
import os

from src.rag.rag_pipeline import ask
from src.rag.retrieval_engine import RetrievalEngine

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

engine = RetrievalEngine()


def ask_question(question: str):

    logger.info(
        f"/ask : {question}"
    )

    return ask(question)


def search_metrics(query: str, top_k: int = 5):

    logger.info(
        f"/search : {query}"
    )

    return engine.search(
        query=query,
        top_k=top_k
    )


def get_all_metrics():

    logger.info(
        "/metrics requested"
    )

    result = (
        supabase
        .table("metrics")
        .select(
            "metric_id,metric_name,abbreviation"
        )
        .order("metric_id")
        .execute()
    )

    unique_metrics = {}

    for row in result.data:

        if row["metric_id"] not in unique_metrics:

            unique_metrics[row["metric_id"]] = row

    return list(unique_metrics.values())


def get_metric_by_id(metric_id: int):

    logger.info(
        f"/metric/{metric_id}"
    )

    result = (
        supabase
        .table("metrics")
        .select("*")
        .eq("metric_id", metric_id)
        .execute()
    )

    return result.data