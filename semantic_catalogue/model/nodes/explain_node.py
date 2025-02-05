from typing import Literal

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END

from semantic_catalogue.common.settings import cfg
from semantic_catalogue.common.utils import format_docs_with_id
from semantic_catalogue.model.chains.fix_generation import fix_chain
from semantic_catalogue.model.chains.generation import generation_chain
from semantic_catalogue.model.chains.hallucination import hallucination_grader_chain
from semantic_catalogue.model.chains.moderation import moderate
from semantic_catalogue.model.logging import logger

chunk_splitter = RecursiveCharacterTextSplitter(
    chunk_size=256,
    chunk_overlap=0,
    separators=["\n\n", "\n", ". "],
    keep_separator=False,
)


def explain_dataset(state):
    """
    Generate an explanation for the given dataset.

    Split a document into chunks, format, and invoke the generation chain.
    Generates a response with inline citations based on the query and document chunks.

    Args:
        state (dict): The state containing the query and document.

    Returns:
        dict: The updated state with the generation, citations, iteration, and document chunks.
    """
    logger.info("Starting explain generation...")
    query = state["query"]
    document = state["document"]

    logger.debug("Splitting document into chunks for citations")
    # splitting into chunks ensures the model can choose specific parts to cite inline
    chunks = chunk_splitter.split_documents([document])
    doc_chunks = format_docs_with_id(chunks)
    logger.debug("Invoking citation chain to generate response")
    out = generation_chain.invoke({"query": query, "context": doc_chunks})
    logger.debug(f"Generation result length: {len(out.generation)}")

    logger.debug(f"Chunks used in citation: {out.citations}")

    return {
        **state,
        "generation": out.generation,
        "citations": out.citations,
        "iteration": 0,
        "doc_chunks": doc_chunks,
    }


def moderate_generation(state):
    """
    Moderate the generated content.

    Invokes the moderation chain to check the generated content for inappropriate
    content and updates the state accordingly.

    Args:
        state (dict): The state containing the generation.

    Returns:
        dict: The updated state with the moderated generation.
    """
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
    """
    Check for hallucinations in the generated content.

    Invokes the hallucination grader chain to evaluate the generated content
    against the original document and updates the state with the hallucination
    status and explanation.

    Args:
        state (dict): The state containing the document and generation.

    Returns:
        dict: The updated state with the hallucination status, explanation, and iteration count.
    """
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
    """
    Determine if the explanation should be regenerated.

    Checks if the generated content contains hallucinations and if the maximum
    iteration count has been reached.

    Args:
        state (dict): The state containing the hallucination status and iteration count.

    Returns:
        Literal["fix_hallucination", END]: The next step in the graph.
    """
    logger.info("Checking if the explanation should be regenerated.")
    if not state["is_hallucination"] or state["iteration"] > cfg.model.max_iterations:
        return END
    logger.info("Hallucination found, regenerating.")
    return "fix_hallucination"


def fix_hallucination(state):
    """
    Attempt to fix hallucinations in the generated content.

    Invokes the fix chain to generate a new response based on the query, document
    chunks, current generation, and explanation.

    Args:
        state (dict): The state containing the query, document chunks, generation, and explanation.

    Returns:
        dict: The updated state with the fixed generation and citations.
    """
    logger.info("Attempting to fix hallucination...")
    out = fix_chain.invoke(
        {
            "query": state["query"],
            "context": state["doc_chunks"],
            "summary": state["generation"],
            "explanation": state["explanation"],
        }
    )
    logger.debug(f"Fixed generation result length: {len(out.generation)}")
    return {**state, "generation": out.generation, "citations": out.citations}


def skip_hallucination(state) -> Literal["check_hallucination", END]:
    """
    Skip the hallucination check if the generation contains inappropriate content.

    Args:
        state (dict): The state containing the generation.

    Returns:
        Literal["check_hallucination", END]: The next step in the graph.
    """
    if state["generation"] != "Inappropriate content found in generation.":
        return "check_hallucination"
    logger.warning("Inappropriate content found in generation.")
    return END
