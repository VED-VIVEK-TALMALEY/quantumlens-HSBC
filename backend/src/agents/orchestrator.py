# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import uuid
from typing import Dict, Optional

from .planner import Planner
from .conversation_memory import ConversationMemory
from .execution_context import ExecutionContext
from .agent_registry import AgentRegistry


class ConversationMemoryStore:
    """Session-isolated store for conversational memory to avoid cross-user state leaks."""

    def __init__(self):
        self._sessions: Dict[str, ConversationMemory] = {}

    def get(self, conversation_id: str) -> ConversationMemory:
        if conversation_id not in self._sessions:
            self._sessions[conversation_id] = ConversationMemory()
        return self._sessions[conversation_id]

    def clear(self, conversation_id: str) -> None:
        self._sessions.pop(conversation_id, None)


class Orchestrator:
    def __init__(self, registry: Optional[AgentRegistry] = None, planner: Optional[Planner] = None):
        self.registry = registry or AgentRegistry()
        self.planner = planner or Planner()
        self.memory_store = ConversationMemoryStore()

    def get_memory(self, conversation_id: Optional[str] = None) -> ConversationMemory:
        cid = conversation_id or "default"
        return self.memory_store.get(cid)

    def execute(self, question: str, conversation_id: Optional[str] = None) -> dict:
        cid = conversation_id or str(uuid.uuid4())
        memory = self.get_memory(cid)

        resolved_question = memory.resolve(question)
        plan = self.planner.plan(resolved_question)
        memory.update(plan, resolved_question)

        context = ExecutionContext(
            question=resolved_question,
            plan=plan,
        )

        for step in plan.steps:
            agent = self.registry.get(step.agent)
            context = agent.execute(context)
            if (
                step.agent == "audit"
                and context.audit_result
                and not context.audit_result.get("valid", True)
            ):
                return {
                    "status": "error",
                    "conversation_id": cid,
                    "confidence": context.audit_result.get("confidence", 0.0),
                    "warnings": context.audit_result.get("warnings", []),
                    "answer": f"Audit verification failed for {plan.metric}. Warnings: {', '.join(context.audit_result.get('warnings', []))}",
                }

        result = self.registry.get("response").execute(context)
        if isinstance(result, dict):
            result["conversation_id"] = cid
        return result


_shared_orchestrator: Optional[Orchestrator] = None


def get_orchestrator() -> Orchestrator:
    """Return the shared orchestrator instance to eliminate redundant agent construction."""
    global _shared_orchestrator
    if _shared_orchestrator is None:
        _shared_orchestrator = Orchestrator()
    return _shared_orchestrator