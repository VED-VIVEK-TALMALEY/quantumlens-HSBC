# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from src.rag.retrieval_engine import retrieve


class RAGAgent:

    def execute(self, question: str):

        context = retrieve(question)

        return context


if __name__ == "__main__":

    rag = RAGAgent()

    result = rag.execute(
        "Explain CET1 ratio"
    )

    print(result)