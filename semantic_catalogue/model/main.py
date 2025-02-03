from semantic_catalogue.model.graph import generation_graph, search_graph
from semantic_catalogue.model.logging import logger


def search(query, thread_id):
    logger.debug(f"Starting search with query: {query} and thread_id: {thread_id}")
    search = search_graph()
    output = search.invoke(
        {"query": query}, config={"configurable": {"thread_id": thread_id}}
    )
    logger.info("Search completed successfully")
    logger.debug(f"Number of documents returned: {len(output['documents'])}")
    return output


def generate(query, document, thread_id):
    logger.debug(
        f"Starting generation with query: {query}, document_id: {document.metadata['id']}, and thread_id: {thread_id}"
    )
    gen = generation_graph()
    output = gen.invoke(
        {"query": query, "document": document},
        config={"configurable": {"thread_id": thread_id}},
    )
    logger.info("Generation completed successfully")
    logger.debug(f"Generation output length: {len(output['generation'])}")
    return output


if __name__ == "__main__":
    query = "AHAH"
    out = search(query=query, thread_id="1234")

    out_gen = generate(query=query, document=out["documents"][0], thread_id="1234")
    out_gen
    [doc.metadata["score"] for doc in out["documents"]]
