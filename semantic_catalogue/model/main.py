from semantic_catalogue.model.graph import generation_graph, search_graph
from semantic_catalogue.model.logging import logger


def search(query, thread_id):
    """
    Search for documents based on a query.

    :param query: The search query string.
    :type query: str
    :param thread_id: The ID of the thread initiating the search.
    :type thread_id: str
    :return: The search results.
    :rtype: dict
    """
    logger.debug(f"Starting search: {query=}, {thread_id=}")
    search = search_graph()
    output = search.invoke(
        {"query": query}, config={"configurable": {"thread_id": thread_id}}
    )
    logger.info("Search completed successfully")
    logger.debug(f"Number of documents returned: {len(output['documents'])}")
    return output


def generate(query, document, thread_id):
    """
    Generate content based on a query and a document.

    :param query: The generation query string.
    :type query: str
    :param document: The document to base the generation on.
    :type document: dict
    :param thread_id: The ID of the thread initiating the generation.
    :type thread_id: str
    :return: The generation results.
    :rtype: dict
    """
    logger.debug(
        f"Starting generation: {query=}, {document.metadata['id']=}, {thread_id=}"
    )
    gen = generation_graph()
    output = gen.invoke(
        {"query": query, "document": document},
        config={"configurable": {"thread_id": thread_id}},
    )
    logger.info("Generation completed")
    logger.debug(f"Generation output length: {len(output['generation'])}")
    return output


if __name__ == "__main__":
    query = "AHAH Index"
    out = search(query=query, thread_id="1234")
    print(out)

    out_gen = generate(query=query, document=out["documents"][0], thread_id="1234")
    print(out_gen)
