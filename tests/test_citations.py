from semantic_catalogue.model.chains.citations import citation_chain


def test_citation_chain():
    query = "test query"
    context = "This is a test dataset snippet."
    result = citation_chain.invoke({"query": query, "context": context})
    assert "generation" in result
    assert isinstance(result["generation"], str)
    assert "citations" in result
    assert isinstance(result["citations"], list)
