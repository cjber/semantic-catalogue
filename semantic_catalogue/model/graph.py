from langgraph.graph import END, START, StateGraph

from semantic_catalogue.model.logging import logger
from semantic_catalogue.model.nodes.explain_node import (
    check_hallucination,
    explain_dataset,
    moderate_generation,
    skip_hallucination,
)
from semantic_catalogue.model.nodes.search_node import search
from semantic_catalogue.model.retrievers.dataset_retriever import dataset_retriever
from semantic_catalogue.model.states import GenerationState, SearchState


def search_graph():
    logger.info("Initializing search graph")
    retriever = dataset_retriever()
    logger.debug("Dataset retriever initialized")

    workflow = StateGraph(SearchState)
    workflow.add_node("search", lambda state: search(state, retriever))

    workflow.add_edge(START, "search")
    workflow.add_edge("search", END)
    return workflow.compile()


def generation_graph():
    logger.info("Initializing generation graph")
    workflow = StateGraph(GenerationState)
    workflow.add_node("explain_dataset", explain_dataset)
    workflow.add_node("moderate_generation", moderate_generation)
    workflow.add_node("check_hallucination", check_hallucination)

    workflow.add_edge(START, "explain_dataset")
    workflow.add_edge("explain_dataset", "moderate_generation")
    workflow.add_conditional_edges("moderate_generation", skip_hallucination)
    workflow.add_edge("check_hallucination", END)
    return workflow.compile()
