import logging
from typing import TypedDict

from dotenv import load_dotenv
from langchain_community.retrievers import PineconeHybridSearchRetriever
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, START, StateGraph
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder

from src.common.settings import cfg
from src.model.citations import answer_citations, format_docs_with_id
from src.model.hallucination import hallucination_grader
from src.model.moderation import moderate

_ = load_dotenv()


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SearchState(TypedDict):
    query: str
    documents: list[str]


class GenerationState(TypedDict):
    query: str
    document: str
    generation: str
    chunks: list[dict]

    hallucination: str
    inappropriate: str


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    separators=["\n\n", "\n", ". "],
    keep_separator=False,
)


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


def create_retriever():
    bm25_encoder = BM25Encoder().load("bm25/bm25_values.json")
    pc = Pinecone()
    index = pc.Index(cfg.datastore.index_name, host=cfg.datastore.host)
    embeddings = OpenAIEmbeddings(model=cfg.datastore.embed_model)
    return PineconeHybridSearchRetriever(
        embeddings=embeddings,
        sparse_encoder=bm25_encoder,
        index=index,
        top_k=cfg.model.top_k,
        alpha=cfg.model.alpha,
    )


def retrieve(state, retriever):
    logging.info("Starting retrieval process...")
    query = state["query"]

    documents = retriever.invoke(query)
    documents = _group_by_document(documents)
    return {"documents": documents, "query": query}


def explain_dataset(state):
    logging.info("Starting explain generation...")
    query = state["query"]
    document = state["document"]

    chunks = text_splitter.split_documents([document])
    docs = format_docs_with_id(chunks)

    generation = answer_citations.invoke({"query": query, "context": docs})

    return {
        "query": query,
        "document": document,
        "chunks": [c.dict() for c in chunks],
    } | generation


def moderate_generation(state):
    logging.info("Starting moderation...")
    generation = state["generation"]

    moderation = moderate.invoke(generation)
    if moderation["output"] != generation:
        logging.warning("Inappropriate content found in generation")
        state["generation"] = "Inappropriate content found in generation."
        state["inappropriate"] = generation
    else:
        logging.info("Generation content is appropriate")

    return state


def check_hallucination(state):
    logging.info("Starting hallucination check process...")
    query = state["query"]
    document = state["document"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"document": document, "generation": generation}
    )
    if score.binary_score == "yes":
        logging.info("No hallucination found in generation")
        state["generation"] = generation
    else:
        logging.warning("Hallucination found in generation")
        state["generation"] = "Hallucination found in generation."

    return state


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
    output = search.invoke(
        {"query": query}, config={"configurable": {"thread_id": thread_id}}
    )
    logging.info("Search done")
    return output


def generate(query, document, thread_id):
    gen = generation_graph()
    output = gen.invoke(
        {"query": query, "document": document},
        config={"configurable": {"thread_id": thread_id}},
    )
    logging.info("Generation done")
    return output


if __name__ == "__main__":
    query = "farming in estonia"
    out = search(query=query, thread_id="1234")

    out_gen = generate(query=query, document=out["documents"][0], thread_id="1234")
