from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


class RetrievalEngine:

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent

        DB_PATH = BASE_DIR / "vector_db"

        self.client = chromadb.PersistentClient(
            path=str(DB_PATH)
        )

        self.collection = self.client.get_collection(
            "hsbc_kpis"
        )

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def search(
        self,
        query,
        top_k=5
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