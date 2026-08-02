    # -------------------------------------------------------------------
    # Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
    # This project and its source code are strictly proprietary.
    # Unauthorized copying, distribution, or use is strictly prohibited.
    # -------------------------------------------------------------------

from .planner import Planner
from .sql_agent import SQLAgent
from .rag_agent import RAGAgent
from .chart_agent import ChartAgent
from src.auditor.data_auditor import DataAuditor
from .response_agent import ResponseAgent
from .llm_agent import LLMAgent
from .conversation_memory import ConversationMemory
from .agent_registry import AgentRegistry
    
class Orchestrator:
        def __init__(self):
            self.registry = AgentRegistry()
            self.planner = Planner()
            self.auditor = DataAuditor()
            self.response = ResponseAgent()
            self.conversation_memory = ConversationMemory()

        def execute(self, question):
            resolved_question = self.conversation_memory.resolve(question)

            plan = self.planner.plan(resolved_question)

            print(plan)   # <-- keep for debugging

            sql_result = None
            chart_result = None
            rag_result = None
            audit_result = None
            llm_result = None

            # ---------------- SQL ----------------

            if "sql" in plan.agents:
                sql_result = self.registry.get("sql").execute(plan)

                audit_result = self.auditor.audit(sql_result)

                if not audit_result["valid"]:
                    return {
                        "status": "error",
                        "confidence": audit_result["confidence"],
                        "warnings": audit_result["warnings"]
                    }

                sql_result = audit_result["clean_rows"]

            # ---------------- Chart ----------------

            if "chart" in plan.agents and sql_result:
                chart_result = self.registry.get("chart").execute(
    plan.metric,
    sql_result
)

            # ---------------- RAG ----------------

            if "rag" in plan.agents:
                rag_result = self.registry.get("rag").execute(question)

            # ---------------- LLM ----------------

            if plan.needs_llm:
                llm_result = self.registry.get("llm").execute(
    question,
    sql_result,
    rag_result
)
                self.conversation_memory.update(plan)

            # ---------------- Response ----------------

            return self.response.execute(
                plan=plan,
                sql_result=sql_result,
                chart_result=chart_result,
                rag_result=rag_result,
                audit_result=audit_result,
                llm_result=llm_result
            )


if __name__ == "__main__":
        orchestrator = Orchestrator()
        
        tests = [

        "Show CET1",

        "Why did it fall?",

        "Show its trend",

        "Explain it",

        "Compare it with Tier1"

    ]
        
        for q in tests:
            print("=" * 70)
            print(q)
            result = orchestrator.execute(q)
            print(result)
            plan = orchestrator.planner.plan(q)

        print(plan)
        print(orchestrator.registry.get("sql"))
        print(orchestrator.registry.get("rag"))
        print(orchestrator.registry.get("chart"))
        print(orchestrator.registry.get("llm"))