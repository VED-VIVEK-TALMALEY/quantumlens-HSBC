# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------

from src.rag.retrieval_engine import retrieve
from src.rag.document_retriever import DocumentRetriever
from .execution_context import ExecutionContext


class RAGAgent:

    def __init__(self):

        self.document_retriever = DocumentRetriever()

    def execute(self, context: ExecutionContext):

        metric_context = retrieve(
            context.question
        )

        document_context = self.document_retriever.retrieve(
            context.question
        )

        context.rag_result = {

            "metrics": metric_context,

            "documents": document_context

        }

        return context


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    from .planner import Planner

    planner = Planner()

    plan = planner.plan("Why did CET1 fall?")

    context = ExecutionContext(

        question="Why did CET1 fall?",

        plan=plan

    )

    rag = RAGAgent()

    context = rag.execute(context)

    print("Metric Results")
    print("=" * 60)
    print(context.rag_result["metrics"])

    print("\nNarrative Results")
    print("=" * 60)
    print(context.rag_result["documents"])