import pytest
from unittest.mock import MagicMock, patch

def test_document_retriever_empty_question_raises():
    with patch("chromadb.PersistentClient") as mock_chroma:
        mock_client = MagicMock()
        mock_chroma.return_value = mock_client
        mock_client.get_or_create_collection.return_value = MagicMock()

        from src.rag.document_retriever import DocumentRetriever
        retriever = DocumentRetriever()

        with pytest.raises(ValueError, match="Question must be a non-empty string."):
            retriever.retrieve("")

        with pytest.raises(ValueError, match="Question must be a non-empty string."):
            retriever.retrieve("   ")

        with pytest.raises(ValueError, match="top_k must be at least 1."):
            retriever.retrieve("valid question", top_k=0)
