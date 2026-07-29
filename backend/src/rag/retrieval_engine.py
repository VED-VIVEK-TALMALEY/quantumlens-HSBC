# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from pathlib import Path

import chromadb
from src.utils.logger import logger
from src.config.settings import settings


class RetrievalEngine:
    def __init__(self):

      DB_PATH = settings.VECTOR_DB_PATH
      
      self.client = chromadb.PersistentClient(
            path=str(DB_PATH)
        )
      self.collection = None
      self.model = None
def get_collection(self):

    if self.collection is None:

        logger.info("Connecting to ChromaDB...")

        self.collection = self.client.get_collection(
            "hsbc_kpis"
        )

    return self.collection
def get_model(self):

    if self.model is None:

        logger.info("Loading embedding model...")

        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    return self.model

def search(
        self,
        query,
        top_k=settings.TOP_K
    ):

        query_embedding = (
    self.get_model()
    .encode(query)
    .tolist()
)
        results = self.get_collection().query(

            query_embeddings=[
                query_embedding
            ],

            n_results=top_k

        )

        matches = []
        for i in range(len(results["documents"][0])):

         matches.append({

        "text": results["documents"][0][i],

        "metadata": results["metadatas"][0][i],

        "distance": results["distances"][0][i]

    })

        logger.info("%d documents retrieved", len(matches))
        return matches


if __name__ == "__main__":

    engine = RetrievalEngine()

    while True:

        question = input("\nAsk > ")

        if question.lower() == "exit":
            break

        result = engine.search(question)

        print("\nRESULTS\n")

        for i in range(
            len(result["documents"][0])
        ):

            print("-" * 60)

            print(result["documents"][0][i])

            print(result["metadatas"][0][i])

            print(
                "Distance:",
                result["distances"][0][i]
            )