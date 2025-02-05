from typing import TypedDict

from langchain_core.documents import Document


class SearchState(TypedDict):
    query: str
    documents: list[str]


class GenerationState(TypedDict):
    query: str
    document: Document

    iteration: int

    generation: str
    explanation: str

    doc_chunks: str
    citations: list[int]

    is_hallucination: str
