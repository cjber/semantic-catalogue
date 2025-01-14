from semantic_catalogue.model.chains.moderation import moderate


def test_moderation_chain():
    input_text = "This is a test input."
    result = moderate.invoke({"input": input_text})
    assert "output" in result
    assert isinstance(result["output"], str)
