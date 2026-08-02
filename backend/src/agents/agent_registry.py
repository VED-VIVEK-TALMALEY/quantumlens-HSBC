# -------------------------------------------------------------------
# Agent Registry
# -------------------------------------------------------------------

from .sql_agent import SQLAgent
from .rag_agent import RAGAgent
from .chart_agent import ChartAgent
from .llm_agent import LLMAgent


class AgentRegistry:

    def __init__(self):

        self.agents = {

            "sql": SQLAgent(),

            "rag": RAGAgent(),

            "chart": ChartAgent(),

            "llm": LLMAgent()

        }

    def get(self, name):

        return self.agents.get(name)

    def register(self, name, agent):

        self.agents[name] = agent