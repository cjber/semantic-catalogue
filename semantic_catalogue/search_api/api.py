from typing import Union
from uuid import UUID, uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.documents import Document

from semantic_catalogue.model.main import generate, search

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

document_store = {}
query_mapping = {}


@app.get("/")
def index() -> dict[str, str]:
    """
    Root endpoint that provides a welcome message.

    :return: A dictionary with a welcome message.
    :rtype: dict[str, str]
    """
    return {"message": "Make a post request to /query."}


@app.post("/query")
async def query(q: str) -> dict[str, Union[UUID, str, list[dict]]]:
    """
    Endpoint to handle search queries.

    :param q: The search query string.
    :type q: str
    :return: A dictionary containing the thread ID, query, and list of documents.
    :rtype: dict[str, Union[UUID, str, list[dict]]]
    """
    thread_id = uuid4()
    out = search(query=q, thread_id=thread_id)

    docs_dict = [d.dict() for d in out["documents"]]
    document_store[thread_id] = docs_dict
    query_mapping[thread_id] = q
    return {"thread_id": thread_id, "query": q, "documents": docs_dict}


@app.get("/explain/{thread_id}")
async def explain(thread_id: UUID, docid: int) -> dict:
    """
    Endpoint to explain a specific document from a previous query.

    :param thread_id: The UUID of the thread.
    :type thread_id: UUID
    :param docid: The document ID within the thread.
    :type docid: int
    :return: A dictionary containing the explanation and the document.
    :rtype: dict
    """
    doc_dict = document_store[thread_id][docid]
    document = Document(
        page_content=doc_dict["page_content"],
        metadata=doc_dict["metadata"],
    )
    query = query_mapping[thread_id]
    out = generate(query=query, document=document, thread_id=thread_id)

    # ensure Document is serialisable
    out["document"] = doc_dict
    return out
