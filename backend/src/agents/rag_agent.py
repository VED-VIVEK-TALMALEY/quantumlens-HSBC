# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from src.rag.retrieval_engine import retrieve
from .execution_context import ExecutionContext


class RAGAgent:

    def execute(self, context: ExecutionContext):

        context.rag_result = retrieve(
            context.question
        )

        return context


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    from .planner import Planner

    planner = Planner()

    plan = planner.plan("Explain CET1 ratio")

    context = ExecutionContext(

        question="Explain CET1 ratio",

        plan=plan

    )

    rag = RAGAgent()

    context = rag.execute(context)

    print(context.rag_result)