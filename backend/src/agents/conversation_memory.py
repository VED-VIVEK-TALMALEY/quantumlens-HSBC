# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley.
# -------------------------------------------------------------------

class ConversationMemory:

    def __init__(self):

        self.last_metric = None
        self.last_intent = None
        self.last_plan = None

    # ---------------------------------------------------------

    def resolve(self, question):

        q = question.lower()

        followup_words = [

            "it",
            "this",
            "that",
            "they",
            "them"

        ]

        if self.last_metric:

            for word in followup_words:

                if f" {word} " in f" {q} ":

                    q = q.replace(word, self.last_metric)

        return q

    # ---------------------------------------------------------

    def update(self, plan):

        self.last_metric = plan.metric
        self.last_intent = plan.intent
        self.last_plan = plan