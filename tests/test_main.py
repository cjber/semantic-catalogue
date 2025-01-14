import pytest
from src.model.main import search

def test_search():
    query = "test query"
    thread_id = "test_thread"
    result = search(query, thread_id)
    assert "documents" in result
    assert isinstance(result["documents"], list)
