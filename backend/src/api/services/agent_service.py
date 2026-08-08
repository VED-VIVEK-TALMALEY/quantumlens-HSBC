# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
#
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from src.agents.orchestrator import Orchestrator


orchestrator = Orchestrator()


def process_question(question: str):
    """
    Send a financial question to the QuantumLens agent orchestrator.
    """

    return orchestrator.execute(question)