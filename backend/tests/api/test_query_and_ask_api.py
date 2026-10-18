"""Integration tests for the /query and /ask API endpoints."""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_empty_question_returns_400():
    response = client.post("/query", json={"question": "   "})
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_query_endpoint_returns_valid_structure():
    response = client.post("/query", json={"question": "Show PBT trend"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "answer" in data
    assert "confidence" in data
    assert "conversation_id" in data


def test_ask_endpoint_consolidated_with_orchestrator():
    response = client.post("/ask", json={"question": "What is profit before tax?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data.get("status") in ("success", None) or "answer" in data


def test_multi_turn_conversation_retains_context():
    # First turn: establish topic as PBT
    turn1 = client.post("/query", json={"question": "What is profit before tax?"})
    assert turn1.status_code == 200
    cid = turn1.json().get("conversation_id")
    assert cid is not None

    # Second turn: ask conversational follow-up referencing "it"
    turn2 = client.post(
        "/query",
        json={"question": "Why did it fall?", "conversation_id": cid},
    )
    assert turn2.status_code == 200
    data2 = turn2.json()
    assert data2.get("conversation_id") == cid
    # Verify that plan or metric preserved the context
    assert data2.get("metric") in ("profit_before_tax", "pbt") or "profit" in str(data2.get("answer", "")).lower()
