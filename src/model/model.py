from typing import TypedDict

from dotenv import load_dotenv
from langchain.retrievers import (
    ContextualCompressionRetriever,
    PineconeHybridSearchRetriever,
)
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain_core.documents import Document
from langchain_core.runnables import chain
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langgraph.graph import END, START, StateGraph
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder

from src.common.settings import cfg
from src.common.utils import Paths, pretty_print_docs
from src.model.block_query import appropriate_grader
from src.model.grader import retrieval_grader
from src.model.hallucination import hallucination_grader
from src.model.moderation import moderate
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
    grouped_id: dict[str, list[Document]] = {}

    for d in documents:
        id = d.metadata["id"]
        if id not in grouped_id:
            grouped_id[id] = []
        grouped_id[id].append(d)

    out_nodes = []
    for doc in grouped_id.values():
        content = "\n--------------------\n".join([d.page_content for d in doc])
        # scores = [d.metadata["score"] for d in doc]
        document = Document(
            page_content=content, metadata=doc[0].metadata  # | {"score": max(scores)}
        )
        out_nodes.append(document)
    return out_nodes


def retrieve(state):
    print("---RETRIEVE---")
    query = state["query"]

    bm25_encoder = BM25Encoder().load(str(Paths.DATA / "bm25_values.json"))

    pc = Pinecone()
    index = pc.Index(cfg.datastore.index_name, host=cfg.datastore.host)
    embeddings = OpenAIEmbeddings(model=cfg.datastore.embed_model)
    retriever = PineconeHybridSearchRetriever(
        embeddings=embeddings,
        sparse_encoder=bm25_encoder,
        index=index,
        top_k=cfg.model.top_k,
    )
    documents = retriever.invoke(query)
    documents = _group_by_document(documents)
    compressor = FlashrankRerank(top_n=cfg.model.top_k)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )

    documents = compression_retriever.invoke(query)
    return {"documents": documents, "query": query}


def generation(state):
    query = state["query"]
    document = state["document"]

    generation = rag_chain.invoke({"query": query, "context": document})
    return {"query": query, "document": document, "generation": generation}


def grade_generation(state):
    query = state["query"]
    document = state["document"]
    generation = state["generation"]

    moderation = moderate.invoke(generation)
    if moderation["output"] != generation:
        return {
            "query": query,
            "document": document,
            "generation": "Inappropriate content found in generation.",
        }

    score = hallucination_grader.invoke(
        {"document": document, "generation": generation}
    )
    if score.binary_score == "yes":
        return {"query": query, "document": document, "generation": generation}
    else:
        return {
            "query": query,
            "document": document,
            "generation": "Hallucination found in generation.",
        }


def search_graph():
    workflow = StateGraph(SearchState)
    workflow.add_node("retrieve", retrieve)

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", END)
    return workflow.compile()


def generation_graph():
    workflow = StateGraph(GenerationState)
    workflow.add_node("gen", generation)
    workflow.add_node("grade_generation", grade_generation)

    workflow.add_edge(START, "gen")
    workflow.add_edge("gen", "grade_generation")
    workflow.add_edge("grade_generation", END)
    return workflow.compile()


query = "pizza"
search = search_graph()
out = search.invoke({"query": query})
# pretty_print_docs(out["documents"])

gen = generation_graph()
gen.invoke({"query": query, "document": out["documents"][80].page_content})
