# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from typing import Optional
from src.agents.orchestrator import get_orchestrator


def process_question(question: str, conversation_id: Optional[str] = None):
    """Send a financial question to the QuantumLens agent orchestrator."""
    orchestrator = get_orchestrator()
    return orchestrator.execute(question, conversation_id=conversation_id)