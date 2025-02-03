import numpy as np
from langchain_core.documents import Document

from semantic_catalogue.model.logging import logger


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
    logger.debug(f"Query for retrieval: {query}")

    documents = retriever.invoke(query)

    logger.debug(f"Retrieved {len(documents)} documents")
    documents = _group_by_document(documents)
    scores = [doc.metadata["score"] for doc in documents]
    quintiles = np.percentile(scores, [0, 20, 40, 60, 80, 100])
    quintile_labels = np.digitize(scores, quintiles) - 1

    for doc, score_quintile in zip(documents, quintile_labels):
        doc.metadata["score_quintile"] = score_quintile
    logger.debug(f"Grouped documents into {len(documents)} groups")
    return {"documents": documents, "query": query}
