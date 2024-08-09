from typing import Union
from uuid import UUID, uuid4

from fastapi import FastAPI
from langchain_core.documents import Document

from src.model.model import generate, search

app = FastAPI()
document_store = {}
query_mapping = {}


@app.get("/")
def index() -> dict[str, str]:
    return {"message": "Make a post request to /query."}


@app.post("/query")
async def query(q: str) -> dict[str, Union[UUID, str, list[dict]]]:
    results_id = uuid4()
    out = search(query=q, thread_id=results_id)

    docs_dict = [d.dict() for d in out["documents"]]
    document_store[results_id] = docs_dict
    query_mapping[results_id] = q
    return {"results_id": results_id, "query": q, "documents": docs_dict}


@app.get("/explain/{results_id}")
async def explain(results_id: UUID, docid: int) -> dict:
    doc_dict = document_store[results_id][docid]
    document = Document(
        page_content=doc_dict["page_content"],
        metadata=doc_dict["metadata"],
    )
    query = query_mapping[results_id]
    out = generate(query=query, document=document, thread_id=results_id)
    generation = out["generation"]

    return {
        "generation": generation,
        "metadata": {
            "results_id": results_id,
            "query": query,
            "related_dataset": doc_dict,
        },
    }
