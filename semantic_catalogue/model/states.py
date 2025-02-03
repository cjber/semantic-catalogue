from typing import TypedDict


class SearchState(TypedDict):
    query: str
    documents: list[str]


class GenerationState(TypedDict):
    query: str
    document: str
    generation: str
    explanation: str
    iteration: int
    cited_chunks: list[dict]

    is_hallucination: str
