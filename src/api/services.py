from supabase import create_client
from dotenv import load_dotenv
import os

from src.rag.rag_pipeline import ask
from src.rag.retrieval_engine import RetrievalEngine

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

engine = RetrievalEngine()


def ask_question(question: str):

    return ask(question)


def search_metrics(query: str, top_k: int = 5):

    return engine.search(
        query=query,
        top_k=top_k
    )


def get_all_metrics():

    result = (
        supabase
        .table("metric_definitions")
        .select(
            "metric_id,metric_name,abbreviation"
        )
        .order("metric_id")
        .execute()
    )

    return result.data
def get_metric_by_id(metric_id: int):

    result = (
        supabase
        .table("metrics")
        .select("*")
        .eq("metric_id", metric_id)
        .execute()
    )

    return result.data