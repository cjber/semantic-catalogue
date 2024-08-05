from uuid import UUID, uuid4

from fastapi import FastAPI
from langchain_core.documents import Document

from src.model.model import generation_graph, search_graph

app = FastAPI()
document_store = {}
query_mapping = {}


search_app = search_graph()
gen_app = generation_graph()


@app.get("/")
def index():
    return {"message": "Make a post request to /query."}


@app.post("/query")
async def query(q: str) -> dict:
    thread_id = uuid4()
    out = search_app.invoke(
        {"query": q}, config={"configurable": {"thread_id": thread_id}}
    )
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
    generation_state = gen_app.invoke(
        {"query": query, "document": document},
        config={"configurable": {"thread_id": thread_id}},
    )
    generation = generation_state["generation"]

    return {
        "generation": generation,
        "metadata": {
            "thread_id": thread_id,
            "query": query,
            "related_dataset": doc_dict,
        },
    }
