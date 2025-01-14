from src.model.logging import logger

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
    logger.info("Starting explain generation...")
    query = state["query"]
    document = state["document"]

    logger.debug(f"Splitting document into chunks for query: {query}")
    chunks = text_splitter.split_documents([document])
    logger.debug(f"Document split into {len(chunks)} chunks")
    # docs = format_docs_with_id(chunks)

    logger.debug("Invoking RAG chain for generation")
    generation = rag_chain.invoke({"query": query, "context": document.page_content})
    logger.debug(f"Generation result: {generation}")

    return {
        "query": query,
        "document": document,
        # "chunks": [c.dict() for c in chunks], # TODO: Might use this for citations
    } | {"generation": generation}


def moderate_generation(state):
    logger.info("Starting moderation...")
    generation = state["generation"]

    logger.debug("Invoking moderation chain")
    moderation = moderate.invoke(generation)
    logger.debug(f"Moderation result: {moderation}")
    if moderation["output"] != generation:
        logger.warning("Inappropriate content found in generation")
        state["generation"] = "Inappropriate content found in generation."
        state["inappropriate"] = generation
    else:
        logger.info("Generation content is appropriate")

    return state


def check_hallucination(state):
    logger.info("Starting hallucination check process...")
    document = state["document"]
    generation = state["generation"]

    logger.debug("Invoking hallucination grader chain")
    score = hallucination_grader_chain.invoke(
        {"document": document, "generation": generation}
    )
    logger.debug(f"Hallucination grading result: {score.binary_score}")
    if score.binary_score == "yes":
        logger.info("No hallucination found in generation")
        state["generation"] = generation
    else:
        logger.warning("Hallucination found in generation")
        state["generation"] = f"**Hallucination found in generation.**\n\n{generation}"
    return state


def skip_hallucination(state):
    if state["generation"] != "Inappropriate content found in generation.":
        return "check_hallucination"
    logger.warning("Inappropriate content found in generation")
    return END
