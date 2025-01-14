from semantic_catalogue.model.chains.hallucination import hallucination_grader_chain


def test_hallucination_grader_chain():
    document = "Water is wet."
    generation = "Water is dry."
    result = hallucination_grader_chain.invoke({"document": document, "generation": generation})
    assert "binary_score" in result
    assert result["binary_score"] in ["yes", "no"]
