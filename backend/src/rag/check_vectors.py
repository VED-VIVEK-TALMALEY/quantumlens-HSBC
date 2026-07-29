# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import chromadb

from src.config.settings import settings

client = chromadb.PersistentClient(
    path=str(settings.VECTOR_DB_PATH)
)

collection = client.get_collection(
    "hsbc_kpis"
)

print("\n========================")
print("ChromaDB Verification")
print("========================")
print("Database :", settings.VECTOR_DB_PATH)
print("Collection :", "hsbc_kpis")
print("Vector Count :", collection.count())
print("========================")