# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from .planner import Planner
from .sql_agent import SQLAgent
from .rag_agent import RAGAgent
from .chart_agent import ChartAgent
from .llm_agent import LLMAgent
from .response_agent import ResponseAgent
from .conversation_memory import ConversationMemory
from .execution_context import ExecutionContext
from .financial_reasoning_agent import FinancialReasoningAgent
from .agent_registry import AgentRegistry

from src.auditor.data_auditor import DataAuditor


class Orchestrator:
    

    def __init__(self):
        self.reasoning = FinancialReasoningAgent()

        self.memory = ConversationMemory()

        self.planner = Planner()

        self.registry = AgentRegistry()
        self._agents = {
    "sql": SQLAgent(),
    "audit": DataAuditor(),
    "financial_reasoning": FinancialReasoningAgent(),
    "rag": RAGAgent(),
    "chart": ChartAgent(),
    "llm": LLMAgent(),
    "response": ResponseAgent(),
}


    def execute(self, question):

    # -----------------------------------------
    # Resolve conversation memory
    # -----------------------------------------
     resolved_question = self.memory.resolve(question)
     plan = self.planner.plan(resolved_question)
     self.memory.update(
            plan,
            resolved_question,
            )
     

    # -----------------------------------------
    # Create ONE shared execution context
    # -----------------------------------------
     context = ExecutionContext(
         question=resolved_question,
         plan=plan
    )

    # -----------------------------------------
    # Execute pipeline
    # -----------------------------------------
     for step in plan.steps:
        agent = self.registry.get(step.agent)
        context = agent.execute(context)
        if (
        step.agent == "audit"
        and not context.audit_result["valid"]
    ):
         return {
            "status": "error",
            "confidence": context.audit_result["confidence"],
            "warnings": context.audit_result["warnings"]
        }

    # -----------------------------------------
    # Final Response
    # -----------------------------------------
     return self.registry.get("response").execute(context)


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    orchestrator = Orchestrator()

    tests = [
        # Edge Cases: Definitions
        "What is CET1 capital?",
        "What is CET1 ratio?",
        "What is Tier 1?",
        "What is Tier 1 ratio?",
        "What is NII?",
        # Edge Cases: Analysis / Why
        "Why did CET1 ratio fall?",
        "Why did CET1 capital fall?",
        "Why did NII increase?",
        "Why did revenue decline?",
        # Edge Cases: Trends
        "Show CET1 trend",
        "Show CET1 ratio trend",
        "Show Tier 1 trend",
        "Show NII trend",
        "Show revenue trend",
        # Edge Cases: Comparisons
        "Compare CET1 capital with CET1 ratio",
        "Compare CET1 ratio with Tier 1 ratio",
        "Compare NII with revenue",
        # Edge Cases: Non-Existent Metrics (EBITDA / Hallucination Checks)
        "Show something that does not exist",
        "What is EBITDA?",
        "Show EBITDA trend",
        "Why did EBITDA fall?",
    ]

    for q in tests:
        print("=" * 70)
        print(f"QUERY: {q}")
        result = orchestrator.execute(q)
        print(result)