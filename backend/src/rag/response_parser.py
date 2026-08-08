## -------------------------------------------------------------------
## Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
##
## This project and its source code are strictly proprietary.
## Unauthorized copying, distribution, or use is strictly prohibited.
## -------------------------------------------------------------------

from datetime import datetime


def parse_response(question, answer, retrieval_result):
    # ---------------------------------------------------------------
    # Current retrieval format
    #
    # engine.search() returns:
    #
    # [
    #     {
    #         "text": "...",
    #         "metadata": {...},
    #         "distance": ...
    #     }
    # ]
    # ---------------------------------------------------------------

    if isinstance(retrieval_result, list):
        sources = []
        retrieved_documents = []
        distances = []

        for document in retrieval_result:
            if not isinstance(document, dict):
                continue

            metadata = document.get("metadata", {})

            text = document.get(
                "text",
                document.get("document", "")
            )

            distance = document.get(
                "distance"
            )

            sources.append(metadata)
            retrieved_documents.append(text)
            distances.append(distance)

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "retrieved_documents": retrieved_documents,
            "distances": distances,
            "generated_at": datetime.now().isoformat()
        }

    # ---------------------------------------------------------------
    # Legacy retrieval format
    #
    # Kept for backward compatibility with older RAG components.
    # ---------------------------------------------------------------

    if isinstance(retrieval_result, dict):
        metadatas = retrieval_result.get(
            "metadatas",
            []
        )

        documents = retrieval_result.get(
            "documents",
            []
        )

        distances = retrieval_result.get(
            "distances",
            []
        )

        # Chroma commonly returns nested lists.
        if metadatas and isinstance(metadatas[0], list):
            metadatas = metadatas[0]

        if documents and isinstance(documents[0], list):
            documents = documents[0]

        if distances and isinstance(distances[0], list):
            distances = distances[0]

        return {
            "question": question,
            "answer": answer,
            "sources": metadatas,
            "retrieved_documents": documents,
            "distances": distances,
            "generated_at": datetime.now().isoformat()
        }

    # ---------------------------------------------------------------
    # Unknown / empty retrieval result
    # ---------------------------------------------------------------

    return {
        "question": question,
        "answer": answer,
        "sources": [],
        "retrieved_documents": [],
        "distances": [],
        "generated_at": datetime.now().isoformat()
    }


## -------------------------------------------------------------------
## Testing
## -------------------------------------------------------------------

if __name__ == "__main__":
    fake_retrieval = [
        {
            "text": "CET1 is a regulatory capital ratio.",
            "metadata": {
                "page": 46,
                "source": "earnings-release.pdf"
            },
            "distance": 0.25
        },
        {
            "text": "CET1 ratio decreased from 14.9% to 14.0%.",
            "metadata": {
                "page": 34,
                "source": "earnings-release.pdf"
            },
            "distance": 0.41
        }
    ]

    result = parse_response(
        question="What is CET1 ratio?",
        answer="CET1 is a regulatory capital ratio.",
        retrieval_result=fake_retrieval
    )

    print(result)