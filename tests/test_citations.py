from semantic_catalogue.model.chains.citations import CitedAnswer, citation_chain


def test_citation_chain():
    query = "test query"
    context = "This is a test dataset snippet."
    result = citation_chain.invoke({"query": query, "context": context})
    assert isinstance(result, CitedAnswer)
    assert hasattr(result, "generation")
    assert hasattr(result, "citations")
    assert isinstance(result.citations, list)
    assert isinstance(result.generation, str)
