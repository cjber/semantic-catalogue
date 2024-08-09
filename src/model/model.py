from typing import TypedDict

from dotenv import load_dotenv
from langchain.retrievers import (
    ContextualCompressionRetriever,
    PineconeHybridSearchRetriever,
)

# from langchain.retrievers.document_compressors import FlashrankRerank
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langgraph.graph import END, START, StateGraph
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder

from src.common.settings import cfg
from src.common.utils import Paths, pretty_print_docs
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
    hallucination: str
    inappropriate: str


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


def create_retriever():
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
    return retriever


def retrieve(state, retriever):
    print("---RETRIEVE---")
    query = state["query"]

    documents = retriever.invoke(query)
    documents = _group_by_document(documents)
    return {"documents": documents, "query": query}


# def compress(state, retriever):
#     print("---COMPRESS---")
#     query = state["query"]
#
#     compressor = FlashrankRerank(top_n=cfg.model.top_k)
#     compression_retriever = ContextualCompressionRetriever(
#         base_compressor=compressor, base_retriever=retriever
#     )
#
#     documents = compression_retriever.invoke(query)
#     return {"documents": documents, "query": query}


def explain_dataset(state):
    print("---GENERATE---")
    query = state["query"]
    document = state["document"]

    generation = rag_chain.invoke({"query": query, "context": document})
    return {"query": query, "document": document, "generation": generation}


def moderate_generation(state):
    print("---MODERATE GENERATION---")
    query = state["query"]
    document = state["document"]
    generation = state["generation"]

    moderation = moderate.invoke(generation)
    if moderation["output"] != generation:
        print("---INAPPROPRIATE---")
        state = {
            "query": query,
            "document": document,
            "generation": "Inappropriate content found in generation.",
            "generation_moderated": moderation["output"],
            "inappropriate": generation,
        }
    else:
        print("---APPROPRIATE---")
        return {"query": query, "document": document, "generation": generation}


def check_hallucination(state):
    print("---CHECK HALLUCINATION---")
    query = state["query"]
    document = state["document"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"document": document, "generation": generation}
    )
    if score.binary_score == "yes":
        print("---NO HALLUCINATATION---")
        return {"query": query, "document": document, "generation": generation}
    else:
        print("---HALLUCINATATION---")
        return {
            "query": query,
            "document": document,
            "generation": "Hallucination found in generation.",
            "hallucination": generation,
        }


def skip_hallucination(state):
    if state["generation"] == "Inappropriate content found in generation.":
        return END
    else:
        return "check_hallucination"


def search_graph():
    retriever = create_retriever()

    workflow = StateGraph(SearchState)
    workflow.add_node("retrieve", lambda state: retrieve(state, retriever))
    # workflow.add_node("compress", lambda state: compress(state, retriever))

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", END)
    # workflow.add_edge("retrieve", "compress")
    # workflow.add_edge("compress", END)
    return workflow.compile()


def generation_graph():
    workflow = StateGraph(GenerationState)
    workflow.add_node("explain_dataset", explain_dataset)
    workflow.add_node("moderate_generation", moderate_generation)
    workflow.add_node("check_hallucination", check_hallucination)

    workflow.add_edge(START, "explain_dataset")
    workflow.add_edge("explain_dataset", "moderate_generation")
    workflow.add_conditional_edges("moderate_generation", skip_hallucination)
    workflow.add_edge("check_hallucination", END)
    return workflow.compile()


def search(query, thread_id):
    search = search_graph()
    search_out = search.invoke(
        {"query": query}, config={"configurable": {"thread_id": thread_id}}
    )
    return search_out


def generate(query, document, thread_id):
    gen = generation_graph()
    gen_out = gen.invoke(
        {"query": query, "document": document},
        config={"configurable": {"thread_id": thread_id}},
    )
    return gen_out


if __name__ == "__main__":
    out = search(query="space travel", thread_id="1234")
    out_gen = generate(
        query="space travel", document=out["documents"][0], thread_id="1234"
    )
