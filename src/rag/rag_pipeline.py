from retrieval_engine import RetrievalEngine
from prompt_builder import build_prompt
from llm_service import ask_llm
from response_parser import parse_response


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