
# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------

import chromadb
from sentence_transformers import SentenceTransformer


class DocumentRetriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="financial_documents"
        )

    def retrieve(
        self,
        question,
        top_k=5
    ):

        embedding = self.model.encode(
            question
        ).tolist()

        results = self.collection.query(

            query_embeddings=[embedding],

            n_results=top_k

        )

        documents = []

        for i in range(

            len(results["documents"][0])

        ):

            documents.append(

                {

                    "text":
                        results["documents"][0][i],

                    "metadata":
                        results["metadatas"][0][i],

                    "distance":
                        results["distances"][0][i]

                }

            )

        return documents


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    retriever = DocumentRetriever()

    docs = retriever.retrieve(

        "Why did CET1 fall?"

    )

    for doc in docs:

        print("=" * 60)

        print(doc)

