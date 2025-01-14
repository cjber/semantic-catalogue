from src.model.logging import logger

from langchain_core.documents import Document


def _group_by_document(documents):
    grouped_id: dict[str, list[Document]] = {}

    for d in documents:
        id = d.metadata["id"]
        if id not in grouped_id:
            grouped_id[id] = []
        grouped_id[id].append(d)

    out_nodes = []
    for doc in grouped_id.values():
        content = "\n\n".join([d.page_content for d in doc])
        scores = [d.metadata["score"] for d in doc]
        document = Document(
            page_content=content, metadata=doc[0].metadata | {"score": max(scores)}
        )
        out_nodes.append(document)
    return out_nodes


def search(state, retriever):
    logger.info("Starting retrieval process...")
    query = state["query"]

    documents = retriever.invoke(query)
    documents = _group_by_document(documents)
    return {"documents": documents, "query": query}
