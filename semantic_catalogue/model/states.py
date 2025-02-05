from typing import TypedDict


class SearchState(TypedDict):
    query: str
    documents: list[str]


class GenerationState(TypedDict):
    query: str
    document: str

    iteration: int

    generation: str
    explanation: str

    doc_chunks: str
    citations: list[int]

    is_hallucination: str
