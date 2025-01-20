from langgraph.graph import END

from semantic_catalogue.model.chains.hallucination import hallucination_grader_chain
from semantic_catalogue.model.chains.moderation import moderate
from semantic_catalogue.model.chains.rag import rag_chain
from semantic_catalogue.model.logging import logger


def explain_dataset(state):
    logger.info("Starting explain generation...")
    query = state["query"]
    document = state["document"]

    logger.debug("Invoking RAG chain for generation")
    generation = rag_chain.invoke({"query": query, "context": document.page_content})
    logger.debug(f"Generation result length: {len(generation)}")

    return {**state, "generation": generation}


def moderate_generation(state):
    logger.info("Starting moderation...")
    generation = state["generation"]

    logger.debug("Invoking moderation chain")
    moderation = moderate.invoke(generation)
    logger.debug(f"Moderation result length: {len(moderation['output'])}")
    if moderation["output"] != generation:
        logger.warning("Inappropriate content found in generation")
        state["generation"] = (
            f"**Inappropriate content found in generation.**\n{generation}"
        )
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
