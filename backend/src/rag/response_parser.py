# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from datetime import datetime


def parse_response(
    question,
    answer,
    retrieval_result
):

    return {

        "question": question,

        "answer": answer,

        "sources": retrieval_result["metadatas"][0],

        "retrieved_documents":
            retrieval_result["documents"][0],

        "distances":
            retrieval_result["distances"][0],

        "generated_at":
            datetime.now().isoformat()

    }