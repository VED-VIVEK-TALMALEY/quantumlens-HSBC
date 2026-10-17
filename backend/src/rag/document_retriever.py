# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import chromadb


class DocumentRetriever:
    def __init__(self):
        self.embedding_service_url = os.getenv(
            "EMBEDDING_SERVICE_URL",
            "http://embedding-service:8001",
        ).rstrip("/")

        vector_db_path = os.getenv("VECTOR_DB_PATH", "chroma_db")
        self.client = chromadb.PersistentClient(
            path=vector_db_path
        )

        self.collection = self.client.get_or_create_collection(
            name="financial_documents"
        )

    def _embed_query(self, question):
        """Generate a query embedding through the embedding microservice."""

        payload = json.dumps({
            "texts": [question]
        }).encode("utf-8")

        request = Request(
            url=f"{self.embedding_service_url}/embed",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=30) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as exc:
            error_body = exc.read().decode(
                "utf-8", errors="replace"
            )
            raise RuntimeError(
                f"Embedding service returned HTTP "
                f"{exc.code}: {error_body}"
            ) from exc

        except URLError as exc:
            raise RuntimeError(
                "Cannot connect to embedding service at "
                f"{self.embedding_service_url}: {exc.reason}"
            ) from exc

        embeddings = result.get("embeddings")

        if not embeddings or not embeddings[0]:
            raise RuntimeError(
                "Embedding service returned no query embedding."
            )

        return embeddings[0]

    def retrieve(self, question, top_k=5):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question must be a non-empty string.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        embedding = self._embed_query(question)

        collection_count = self.collection.count()

        if collection_count == 0:
            return []

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=min(top_k, collection_count),
            include=["documents", "metadatas", "distances"],
        )

        documents = []

        result_documents = results.get("documents") or [[]]
        result_metadatas = results.get("metadatas") or [[]]
        result_distances = results.get("distances") or [[]]

        for i, text in enumerate(result_documents[0] or []):
            metadata_rows = result_metadatas[0] or []
            distance_rows = result_distances[0] or []

            documents.append({
                "text": text,
                "metadata": (
                    metadata_rows[i]
                    if i < len(metadata_rows)
                    else {}
                ),
                "distance": (
                    distance_rows[i]
                    if i < len(distance_rows)
                    else None
                ),
            })

        return documents


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":
    retriever = DocumentRetriever()

    docs = retriever.retrieve("Why did CET1 fall?")

    for doc in docs:
        print("=" * 60)
        print(doc)