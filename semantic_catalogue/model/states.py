from typing import TypedDict


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
