import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END

from src.common.utils import format_docs_with_id
from src.model.chains.hallucination import hallucination_grader_chain
from src.model.chains.moderation import moderate
from src.model.chains.rag import rag_chain

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    separators=["\n\n", "\n", ". "],
    keep_separator=False,
)


def explain_dataset(state):
    # TODO: Might use chunks for citations
    logging.info("Starting explain generation...")
    query = state["query"]
    document = state["document"]

    chunks = text_splitter.split_documents([document])
    # docs = format_docs_with_id(chunks)

    generation = rag_chain.invoke({"query": query, "context": document.page_content})

    return {
        "query": query,
        "document": document,
        # "chunks": [c.dict() for c in chunks], # TODO: Might use this for citations
    } | {"generation": generation}


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
    document = state["document"]
    generation = state["generation"]

    score = hallucination_grader_chain.invoke(
        {"document": document, "generation": generation}
    )
    if score.binary_score == "yes":
        logging.info("No hallucination found in generation")
        state["generation"] = generation
    else:
        logging.warning("Hallucination found in generation")
        state["generation"] = f"**Hallucination found in generation.**\n\n{generation}"
    return state


def skip_hallucination(state):
    if state["generation"] != "Inappropriate content found in generation.":
        return "check_hallucination"
    logging.warning("Inappropriate content found in generation")
    return END
