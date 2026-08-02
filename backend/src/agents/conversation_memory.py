# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------


class ConversationMemory:

    def __init__(self):
        self.last_metric = None
        self.last_intent = None

    def update(self, plan):

        if plan.metric:
            self.last_metric = plan.metric

        self.last_intent = plan.intent

    def resolve(self, query):

        q = query.lower()

        pronouns = [
            "it",
            "that",
            "this",
            "same"
        ]

        if self.last_metric is None:
            return query

        for p in pronouns:
            q = q.replace(p, self.last_metric)

        return q

    def clear(self):
        self.last_metric = None
        self.last_intent = None


if __name__ == "__main__":

    memory = ConversationMemory()

    print(memory.resolve("Why did it fall?"))

    class DummyPlan:
        metric = "cet1"
        intent = "metric_lookup"

    memory.update(DummyPlan())

    print(memory.resolve("Why did it fall?"))
    print(memory.resolve("Compare it with Tier1"))