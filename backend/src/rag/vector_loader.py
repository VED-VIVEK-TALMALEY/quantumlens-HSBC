# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import json


import chromadb

from src.utils.logger import logger
from src.config.settings import settings

def load_embeddings():

    with open(
        settings.EMBEDDINGS_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ----------------------------------------
# Connect to ChromaDB
# ----------------------------------------

def load_vectors():

    logger.info("Loading vectors...")

    embeddings = load_embeddings()

    client = chromadb.PersistentClient(
        path=str(settings.VECTOR_DB_PATH)
    )

    try:
        client.delete_collection("hsbc_kpis")
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name="hsbc_kpis"
    )

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
                        "metric_id": record["metric_id"],
                        "metric_name": record["metric_name"],
                        "abbreviation": record["abbreviation"],
                        "sheet_name": record["sheet_name"],
                        "source_workbook": record["source_workbook"],
                        "row_number": record["row_number"]
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

    logger.info(
        f"{collection.count()} vectors in ChromaDB"
    )
    return collection

def load_vector_db():
    return load_vectors()


if __name__ == "__main__":

    load_vectors()