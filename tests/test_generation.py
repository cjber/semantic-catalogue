from semantic_catalogue.model.main import generate
from langchain_core.documents import Document


def test_generate():
    query = "healthy food"
    document = Document(page_content="This is a test document.", metadata={"id": "test_id"})
    thread_id = "test_thread"
    result = generate(query, document, thread_id)
    assert "generation" in result
    assert isinstance(result["generation"], str)
