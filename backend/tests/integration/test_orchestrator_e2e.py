"""End-to-end tests for the multi-agent orchestrator, vector databases, and memory isolation."""
import pytest
import chromadb
from src.config.settings import settings
from src.agents.orchestrator import get_orchestrator, Orchestrator


def test_canonical_vectordb_collections_exist():
    """Verify both hsbc_kpis and financial_documents collections are intact at canonical path."""
    client = chromadb.PersistentClient(path=str(settings.VECTOR_DB_PATH))
    collection_names = [c.name for c in client.list_collections()]
    assert "hsbc_kpis" in collection_names, f"hsbc_kpis missing from {collection_names}"
    assert "financial_documents" in collection_names, f"financial_documents missing from {collection_names}"

    kpis_count = client.get_collection("hsbc_kpis").count()
    docs_count = client.get_collection("financial_documents").count()
    assert kpis_count > 0, "hsbc_kpis collection is empty"
    assert docs_count > 0, "financial_documents collection is empty"


def test_orchestrator_pbt_trend_execution():
    """Verify that a PBT question executes through Planner, SQL, Audit, Financial Reasoning, and Formatter."""
    orchestrator = get_orchestrator()
    result = orchestrator.execute("Show PBT trend")
    assert result["status"] == "success"
    assert result["metric"] in ("profit_before_tax", "pbt")
    assert "answer" in result
    assert result["confidence"] >= 0.8
    assert "chart" in result


def test_conversation_memory_session_isolation():
    """Verify that conversation memory is strictly partitioned per conversation_id."""
    orchestrator = Orchestrator()

    # Session A sets context to PBT
    orchestrator.execute("What is PBT?", conversation_id="session-user-A")
    mem_a = orchestrator.get_memory("session-user-A")
    assert mem_a.last_metric in ("profit_before_tax", "pbt")

    # Session B has separate context
    orchestrator.execute("What is NII?", conversation_id="session-user-B")
    mem_b = orchestrator.get_memory("session-user-B")
    assert mem_b.last_metric in ("net_interest_income", "nii")

    # Follow-up in Session A resolves to PBT, not NII
    resolved_a = mem_a.resolve("Why did it change?")
    assert "profit_before_tax" in resolved_a or "pbt" in resolved_a
    assert "nii" not in resolved_a
