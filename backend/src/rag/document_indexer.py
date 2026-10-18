
# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------

import uuid

import chromadb
from sentence_transformers import SentenceTransformer
from src.config.settings import settings


class DocumentIndexer:

    def __init__(self, vector_db_path=None):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        db_path = str(vector_db_path or settings.VECTOR_DB_PATH)
        self.client = chromadb.PersistentClient(
            path=db_path
        )

        self.collection = self.client.get_or_create_collection(
            name="financial_documents"
        )

    def index(self, chunks):

        texts = [
            c["text"]
            for c in chunks
        ]

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        ).tolist()

        ids = [
            str(uuid.uuid4())
            for _ in chunks
        ]

        metadatas = []

        for chunk in chunks:

            metadatas.append(

                {
                    "page": chunk["page"],
                    "source": chunk["source"]
                }

            )

        self.collection.add(

            ids=ids,

            documents=texts,

            embeddings=embeddings,

            metadatas=metadatas

        )

        print(
            f"Indexed {len(chunks)} narrative chunks."
        )


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    from document_ingestion import DocumentIngestion
    from document_chunker import DocumentChunker

    ingestion = DocumentIngestion()

    pages = ingestion.ingest(
        "data/HSBC_Q1_2026_Earnings_Release.pdf"
    )

    chunker = DocumentChunker()

    chunks = chunker.chunk(pages)

    indexer = DocumentIndexer()

    indexer.index(chunks)

