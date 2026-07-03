from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from src.config.settings import settings


class RetrievalEngine:

    def __init__(self):

      DB_PATH = settings.VECTOR_DB_PATH
      
      self.client = chromadb.PersistentClient(
            path=str(DB_PATH)
        )

      self.collection = self.client.get_collection(
            "hsbc_kpis"
        )

      self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def search(
        self,
        query,
        top_k=settings.TOP_K
    ):

        query_embedding = self.model.encode(
            query
        ).tolist()

        results = self.collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=top_k

        )

        return results


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