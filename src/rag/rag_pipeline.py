from src.rag.retrieval_engine import RetrievalEngine
from src.rag.prompt_builder import build_prompt
from src.rag.llm_service import ask_llm
from src.rag.response_parser import parse_response

engine = RetrievalEngine()


def ask(question):

    retrieval = engine.search(
        question,
        top_k=5
    )

    prompt = build_prompt(
        question,
        retrieval["documents"][0]
    )

    answer = ask_llm(
        prompt
    )

    return parse_response(
        question,
        answer,
        retrieval
    )


if __name__ == "__main__":

    while True:

        q = input("\nQuestion: ")

        if q.lower() == "exit":
            break

        result = ask(q)

        print("\nAnswer\n")
        print(result["answer"])