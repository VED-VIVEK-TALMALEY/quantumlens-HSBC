from src.rag.rag_pipeline import ask
from src.rag.retrieval_engine import RetrievalEngine

engine = RetrievalEngine()


def ask_question(question: str):

    return ask(question)


def search_metrics(query: str, top_k: int = 5):

    return engine.search(
        query=query,
        top_k=top_k
    )