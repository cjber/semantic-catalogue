from typing import Union
from uuid import UUID, uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.documents import Document

from src.model.model import generate, search

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
    return {"message": "Make a post request to /query."}


@app.post("/query")
async def query(q: str) -> dict[str, Union[UUID, str, list[dict]]]:
    thread_id = uuid4()
    out = search(query=q, thread_id=thread_id)

    docs_dict = [d.dict() for d in out["documents"]]
    document_store[thread_id] = docs_dict
    query_mapping[thread_id] = q
    return {"thread_id": thread_id, "query": q, "documents": docs_dict}


@app.get("/explain/{thread_id}")
async def explain(thread_id: UUID, docid: int) -> dict:
    doc_dict = document_store[thread_id][docid]
    document = Document(
        page_content=doc_dict["page_content"],
        metadata=doc_dict["metadata"],
    )
    query = query_mapping[thread_id]
    out = generate(query=query, document=document, thread_id=thread_id)
    out["document"] = doc_dict

    return out
