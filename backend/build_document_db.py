from src.rag.document_ingestion import DocumentIngestion
from src.rag.document_chunker import DocumentChunker
from src.rag.document_indexer import DocumentIndexer

ingestion = DocumentIngestion()
pages = ingestion.ingest("C:\\Users\\talma\\Desktop\\chart and diag\\quantumlens-HSBC\\backend\\data\\raw\\260505-1q-2026-earnings-release.pdf")

chunker = DocumentChunker()
chunks = chunker.chunk(pages)

indexer = DocumentIndexer()
indexer.index(chunks)