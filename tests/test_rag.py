from semantic_catalogue.model.chains.rag import rag_chain


def test_rag_chain():
    query = "healthy food"
    context = "This is a dataset description related to healthy food."
    result = rag_chain.invoke({"query": query, "context": context})
    assert isinstance(result, str)
