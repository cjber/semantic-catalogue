from typing import Literal

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END

from semantic_catalogue.common.settings import cfg
from semantic_catalogue.common.utils import format_docs_with_id
from semantic_catalogue.model.chains.citations import citation_chain
from semantic_catalogue.model.chains.fix import fix_chain
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
    logger.info("Starting explain generation...")
    query = state["query"]
    document = state["document"]

    logger.debug("Splitting document into chunks for citations")
    # splitting into chunks ensures the model can choose specific parts to cite inline
    chunks = chunk_splitter.split_documents([document])
    doc_chunks = format_docs_with_id(chunks)
    logger.debug("Invoking citation chain to generate response")
    out = citation_chain.invoke({"query": query, "context": doc_chunks})
    logger.debug(f"Generation result length: {len(out.generation)}")

    cited_chunks = [
        chunk.model_dump() for id, chunk in enumerate(chunks) if id in out.citations
    ]
    logger.debug(f"{len(cited_chunks)} chunks used in citation: {out.citations}")

    return {
        **state,
        "generation": out.generation,
        "iteration": 0,
        "cited_chunks": cited_chunks,
    }


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
    if not state["is_hallucination"] or state["iteration"] > cfg.model.max_iterations:
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
