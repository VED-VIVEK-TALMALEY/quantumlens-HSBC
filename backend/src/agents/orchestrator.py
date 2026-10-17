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
        resolved_question = self.memory.resolve(question)
        plan = self.planner.plan(resolved_question)
        self.memory.update(plan, resolved_question)

        context = ExecutionContext(
            question=resolved_question,
            plan=plan,
        )

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
                    "warnings": context.audit_result["warnings"],
                }

        return self.registry.get("response").execute(context)