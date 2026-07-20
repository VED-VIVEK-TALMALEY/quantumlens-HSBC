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