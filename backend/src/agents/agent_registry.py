# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------

from .sql_agent import SQLAgent
from .rag_agent import RAGAgent
from .chart_agent import ChartAgent
from .llm_agent import LLMAgent
from .response_agent import ResponseAgent
from .financial_reasoning_agent import FinancialReasoningAgent

from src.auditor.data_auditor import DataAuditor


class AgentRegistry:

    def __init__(self):

        self._agents = {

            "sql": SQLAgent(),

            "audit": DataAuditor(),

            "financial_reasoning": FinancialReasoningAgent(),

            "rag": RAGAgent(),

            "chart": ChartAgent(),

            "llm": LLMAgent(),

            "response": ResponseAgent(),

        }

    def get(self, name):

        if name not in self._agents:
            raise ValueError(f"Unknown agent: {name}")

        return self._agents[name]