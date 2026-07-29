# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

"""
QuantumLens Vector Database Builder

Single entry point for creating the complete ChromaDB
from the processed KPI records.

Usage:
    python -m src.rag.build_vectordb
"""

import sys
import time

import chromadb

from src.config.settings import settings
from src.rag.embedding_generator import generate_embeddings
from src.rag.vector_loader import load_vectors
from src.utils.logger import logger


def verify_database() -> bool:
    """
    Verify that the Chroma database has been created correctly.
    """

    client = chromadb.PersistentClient(
        path=str(settings.VECTOR_DB_PATH)
    )

    collections = client.list_collections()

    if not collections:
        return False

    collection = client.get_collection("hsbc_kpis")

    count = collection.count()

    print("\n==============================")
    print("Vector Database Verification")
    print("==============================")
    print(f"Collection : hsbc_kpis")
    print(f"Vectors    : {count}")
    print("==============================\n")

    return count > 0


def build():
    """
    Complete Vector DB Build Pipeline.
    """

    start = time.time()

    print("\n===================================")
    print(" QuantumLens Vector Builder")
    print("===================================\n")

    logger.info("Starting Vector Database Build")

    # -----------------------------------
    # Step 1
    # -----------------------------------

    print("[1/3] Generating Embeddings...\n")

    generate_embeddings()

    # -----------------------------------
    # Step 2
    # -----------------------------------

    print("\n[2/3] Loading into ChromaDB...\n")

    load_vectors()

    # -----------------------------------
    # Step 3
    # -----------------------------------

    print("\n[3/3] Verifying Database...\n")

    if not verify_database():

        logger.error("Vector Database verification failed.")

        print("\n❌ Build Failed")

        sys.exit(1)

    elapsed = round(time.time() - start, 2)

    logger.info("Vector Database Build Completed")

    print("===================================")
    print("✅ BUILD SUCCESSFUL")
    print("===================================")
    print(f"Elapsed Time : {elapsed} sec")
    print("===================================\n")


if __name__ == "__main__":
    build()