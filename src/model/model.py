from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langgraph.graph import END, START, StateGraph

from src.common.settings import cfg
from src.model.grader import retrieval_grader
from src.model.hallucination import hallucination_grader
from src.model.rag import rag_chain

_ = load_dotenv()


class SearchState(TypedDict):
    query: str
    documents: list[str]


class GenerationState(TypedDict):
    query: str
    document: str
    generation: str


def _group_by_document(documents):
    grouped_id: dict[str, list[tuple[Document, float]]] = {}

    for node, score in documents:
        id = node.metadata["id"]
        if id not in grouped_id:
            grouped_id[id] = []
        grouped_id[id].append((node, score))

    out_nodes = []
    for group in grouped_id.values():
        nodes = [n[0] for n in group]
        scores = [n[1] for n in group]
        content = "\n--------------------\n".join([n.page_content for n in nodes])
        document = Document(
            page_content=content, metadata=nodes[0].metadata | {"score": max(scores)}
        )
        out_nodes.append(document)
    return out_nodes


def retrieve(state):
    print("---RETRIEVE---")
    embeddings = OpenAIEmbeddings(model=cfg.datastore.embed_model)
    vectorstore = PineconeVectorStore(
        index_name=cfg.datastore.index_name,
        embedding=embeddings,
    )
    query = state["query"]
    documents = vectorstore.similarity_search_with_score(query=query, k=cfg.model.top_k)
    documents = _group_by_document(documents)
    return {"documents": documents, "query": query}


def grade_documents(state):
    print("---CHECK DOCUMENT RELEVANCE TO QUERY---")
    query = state["query"]
    documents = state["documents"]

    filtered_docs = []
    for d in documents:
        score = retrieval_grader.invoke({"query": query, "document": d.page_content})
        grade = score.binary_score  # type: ignore
        if grade == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            continue
    return {"documents": filtered_docs, "query": query}


def generation(state):
    query = state["query"]
    document = state["document"]

    generation = rag_chain.invoke({"query": query, "context": document})
    return {"query": query, "document": document, "generation": generation}


def grade_generation(state):
    query = state["query"]
    document = state["document"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"document": document, "generation": generation}
    )
    grade = score.binary_score

    if grade == "yes":
        return {"query": query, "document": document, "generation": generation}
    else:
        return {"query": query, "document": document, "generation": "Hallucination"}


def search_graph():
    workflow = StateGraph(SearchState)
    workflow.add_node("retrieve", retrieve)
    # workflow.add_node("grade_documents", grade_documents)

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", END)
    # workflow.add_edge("retrieve", "grade_documents")
    # workflow.add_edge("grade_documents", END)
    return workflow.compile()


def generation_graph():
    workflow = StateGraph(GenerationState)
    workflow.add_node("gen", generation)
    workflow.add_node("grade_generation", grade_generation)

    workflow.add_edge(START, "gen")
    workflow.add_edge("gen", "grade_generation")
    workflow.add_edge("grade_generation", END)
    return workflow.compile()


search_app = search_graph()
thread_id = 42
q = "What is the capital of France?"

out = search_app.invoke({"query": q}, config={"configurable": {"thread_id": thread_id}})
[d.dict() for d in out["documents"]]
