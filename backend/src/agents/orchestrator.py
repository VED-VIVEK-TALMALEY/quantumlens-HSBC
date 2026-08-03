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

from src.auditor.data_auditor import DataAuditor


class Orchestrator:

    def __init__(self):

        self.memory = ConversationMemory()

        self.planner = Planner()

        self.sql = SQLAgent()

        self.auditor = DataAuditor()

        self.chart = ChartAgent()

        self.rag = RAGAgent()

        self.llm = LLMAgent()

        self.response = ResponseAgent()

    def execute(self, question):

        # -----------------------------------------
        # Resolve conversation memory
        # -----------------------------------------

        resolved_question = self.memory.resolve(question)

        # -----------------------------------------
        # Planning
        # -----------------------------------------

        plan = self.planner.plan(resolved_question)

        self.memory.update(plan)

        # -----------------------------------------
        # Shared Execution Context
        # -----------------------------------------

        context = ExecutionContext(

            question=resolved_question,

            plan=plan

        )

        # -----------------------------------------
        # SQL
        # -----------------------------------------

        if "sql" in plan.agents:

            context = self.sql.execute(context)

            context = self.auditor.execute(context)

            if not context.audit_result["valid"]:

                return {

                    "status": "error",

                    "confidence": context.audit_result["confidence"],

                    "warnings": context.audit_result["warnings"]

                }

        # -----------------------------------------
        # Chart
        # -----------------------------------------

        if "chart" in plan.agents:

            context = self.chart.execute(context)

        # -----------------------------------------
        # RAG
        # -----------------------------------------

        if "rag" in plan.agents:

            context = self.rag.execute(context)

        # -----------------------------------------
        # LLM
        # -----------------------------------------

        if "llm" in plan.agents:

            context = self.llm.execute(context)

        # -----------------------------------------
        # Final Response
        # -----------------------------------------

        return self.response.execute(context)


# -------------------------------------------------------------------
# Testing
# -------------------------------------------------------------------

if __name__ == "__main__":

    orchestrator = Orchestrator()

    tests = [

        "Show CET1",

        "Show CET1 trend",

        "Explain CET1 ratio",

        "Why did CET1 fall?",

        "Compare it with Tier1",

        "Why did it fall?"

    ]

    for q in tests:

        print("=" * 70)

        print(q)

        result = orchestrator.execute(q)

        print(result)