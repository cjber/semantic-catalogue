from semantic_catalogue.model.chains.hallucination import hallucination_grader_chain


def test_hallucination_grader_chain():
    document = "Water is wet."
    generation = "Water is dry."

    result = hallucination_grader_chain.invoke(
        {"document": document, "generation": generation}
    )
    assert hasattr(result, "binary_score")
    assert result.binary_score in [1, 0]
