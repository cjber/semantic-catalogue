from semantic_catalogue.model.chains.grader import grader_chain


def test_grader_chain():
    document = "This is a relevant document."
    query = "relevant"
    result = grader_chain.invoke({"document": document, "query": query})
    assert hasattr(result, "binary_score")
    assert result.binary_score in ["yes", "no"]
