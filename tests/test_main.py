import nltk

from semantic_catalogue.model.main import search

nltk.download("punkt_tab")


def test_search():
    query = "test query"
    thread_id = "test_thread"
    result = search(query, thread_id)
    assert "documents" in result
    assert isinstance(result["documents"], list)
