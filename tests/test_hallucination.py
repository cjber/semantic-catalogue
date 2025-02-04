from semantic_catalogue.model.chains.hallucination import (
    HallucinationChecker,
    hallucination_grader_chain,
)


def test_hallucination_grader_chain():
    document = "Water is wet."
    generation = "Water is dry."

    result = hallucination_grader_chain.invoke(
        {"document": document, "generation": generation}
    )
    assert isinstance(result, HallucinationChecker)
    assert hasattr(result, "score")
    assert result.score in [1, 0]
