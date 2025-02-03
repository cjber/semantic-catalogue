from typing import Literal

from langgraph.graph import END

from semantic_catalogue.model.chains.fix import fix_chain
from semantic_catalogue.model.chains.hallucination import hallucination_grader_chain
from semantic_catalogue.model.chains.moderation import moderate
from semantic_catalogue.model.chains.rag import rag_chain
from semantic_catalogue.model.logging import logger

MAX_ITERATIONS = 3


def explain_dataset(state):
    logger.info("Starting explain generation...")
    query = state["query"]
    document = state["document"]

    logger.debug("Invoking RAG chain for generation")
    generation = rag_chain.invoke({"query": query, "context": document.page_content})
    logger.debug(f"Generation result length: {len(generation)}")

    return {**state, "generation": generation, "iteration": 0}


def moderate_generation(state):
    logger.info("Starting moderation...")
    generation = state["generation"]

    logger.debug("Invoking moderation chain")
    moderation = moderate.invoke(generation)
    logger.debug(f"Moderation result length: {len(moderation['output'])}")
    if moderation["output"] != generation:
        logger.warning("Inappropriate content found in generation")
        state["generation"] = "Inappropriate content found in generation."
    else:
        logger.info("Generation content is appropriate")
    return state


def check_hallucination(state):
    logger.info("Starting hallucination check process...")

    logger.debug("Invoking hallucination grader chain")
    score = hallucination_grader_chain.invoke(
        {"document": state["document"], "generation": state["generation"]}
    )

    state["is_hallucination"] = not bool(score.score)
    state["explanation"] = score.explanation
    state["iteration"] += 1
    logger.debug(f"Hallucination grading result: {state['is_hallucination']}")
    return state


def should_regenerate(state) -> Literal["fix_hallucination", END]:
    logger.info("Checking if the explanation should be regenerated.")
    if not state["is_hallucination"] or state["iteration"] > MAX_ITERATIONS:
        return END
    logger.info("Hallucination found, regenerating.")
    return "fix_hallucination"


def fix_hallucination(state):
    logger.info("Attempting to fix hallucination...")
    generation = fix_chain.invoke(
        {
            "query": state["query"],
            "context": state["document"].page_content,
            "summary": state["generation"],
            "explanation": state["explanation"],
        }
    )
    logger.debug(f"Fixed generation result length: {len(generation)}")
    return {**state, "generation": generation}


def skip_hallucination(state) -> Literal["check_hallucination", END]:
    if state["generation"] != "Inappropriate content found in generation.":
        return "check_hallucination"
    logger.warning("Inappropriate content found in generation.")
    return END
