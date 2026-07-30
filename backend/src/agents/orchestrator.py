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
class Orchestrator:
    def __init__(self):
        self.planner = Planner()
        self.sql = SQLAgent()
        self.rag = RAGAgent()
        self.chart = ChartAgent()
        self.auditor = DataAuditor()
        self.response = ResponseAgent()

    def execute(self, question):
        plan = self.planner.plan(question)
        
        # Initialize default payload values
        rows = None
        chart = None
        context = None
        confidence = 1.0
        warnings = []
        sql_result = None
        audit_result = None
        rag_result = None

        # 1. SQL & Audit Phase
        if "sql" in plan.agents:
            sql_result = self.sql.execute(plan)
            audit = self.auditor.audit(sql_result)
            sql_result = self.sql.execute(plan)
            
            # Stop execution if data is invalid
            if not audit["valid"]:
                return {
                    "status": "error",
                    "confidence": audit["confidence"],
                    "warnings": audit["warnings"]
                }
            
            # Extract clean data for downstream agents
            rows = audit["clean_rows"]
            confidence = audit["confidence"]
            warnings = audit["warnings"]

        # 2. Downstream Agents (Only run if we have clean rows or don't need SQL)
        if "chart" in plan.agents and rows:
            chart = self.chart.execute(plan.metric, rows)

        if "rag" in plan.agents:
            context = self.rag.execute(question)

        if sql_result:

             audit_result = self.auditor.audit(sql_result)

        if not audit_result["valid"]:

            return {

            "status": "error",

            "confidence": audit_result["confidence"],

            "warnings": audit_result["warnings"]

        }

        sql_result = audit_result["clean_rows"]    
        chart_result = None

        if "chart" in plan.agents:
            chart_result = self.chart.execute(
            plan.metric,
        sql_result
    )
           

        if "rag" in plan.agents:

            rag_result = self.rag.execute(question)
            return self.response.execute(

    plan,

    sql_result=sql_result,

    chart_result=chart_result,

    rag_result=rag_result,

    audit_result=audit_result

)

        # 3. Final Response Assembly
           

if __name__ == "__main__":
    orchestrator = Orchestrator()
    
    tests = [
        "Show CET1",
        "Show CET1 trend",
        "Explain CET1 ratio",
        "Why did CET1 fall?"
    ]
    
    for q in tests:
        print("=" * 70)
        print(q)
        result = orchestrator.execute(q)
        print(result)