import json
import chromadb
from pathlib import Path

# ----------------------------------------
# Load Embeddings
# ----------------------------------------

def load_embeddings(path="embeddings.json"):

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------------------
# Connect to ChromaDB
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parent
def get_collection():
    client = chromadb.PersistentClient(
    path=str(BASE_DIR / "vector_db")
)

    collection = client.get_or_create_collection(
        name="hsbc_kpis"
    )

    return collection


# ----------------------------------------
# Load Embeddings into ChromaDB
# ----------------------------------------

def load_vectors():

    embeddings = load_embeddings()

    collection = get_collection()

    loaded = 0
    failed = 0

    for idx, record in enumerate(embeddings):

        try:

            collection.add(

                ids=[
                    f"{record['metric_id']}_{idx}"
                ],

                embeddings=[
                    record["embedding"]
                ],

                documents=[
                    record["text"]
                ],

                metadatas=[
    {

        "metric_id":
            record["metric_id"],

        "metric_name":
            record["metric_name"],

        "abbreviation":
            record["abbreviation"],

        "sheet_name":
            record["sheet_name"],

        "source_workbook":
            record["source_workbook"],

        "row_number":
            record["row_number"]

    }
]
            )

            loaded += 1

        except Exception as e:

            failed += 1

            print(
                f"Failed Record {idx} "
                f"(Metric {record['metric_id']}): {e}"
            )

    print("\n---------------------------")
    print("Vector Loading Completed")
    print("---------------------------")
    print(f"Loaded : {loaded}")
    print(f"Failed : {failed}")
    print(f"Collection Count : {collection.count()}")


# ----------------------------------------
# Main
# ----------------------------------------

if __name__ == "__main__":

    load_vectors()