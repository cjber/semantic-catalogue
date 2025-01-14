from src.model.logging import logger

from dotenv import load_dotenv

from src.model.graph import generation_graph, search_graph

_ = load_dotenv()




def search(query, thread_id):
    search = search_graph()
    output = search.invoke(
        {"query": query}, config={"configurable": {"thread_id": thread_id}}
    )
    logger.info("Search done")
    return output


def generate(query, document, thread_id):
    gen = generation_graph()
    output = gen.invoke(
        {"query": query, "document": document},
        config={"configurable": {"thread_id": thread_id}},
    )
    logger.info("Generation done")
    return output


if __name__ == "__main__":
    query = "healthy food"
    out = search(query=query, thread_id="1234")

    out_gen = generate(query=query, document=out["documents"][0], thread_id="1234")
