from langchain import hub

from semantic_catalogue.model.chains.generation import CitedAnswer
from semantic_catalogue.model.llms.llm import LLM

prompt = hub.pull("cjber/regeneration-with-citations")

SLLM = LLM.with_structured_output(CitedAnswer)
fix_chain = prompt | SLLM

if __name__ == "__main__":
    test_query = "healthy food"
    test_context = """
AHAH (the index of ‘Access to Healthy Assets and Hazards’) is a multi-dimensional index developed by the CDRC for Great Britain measuring how ‘healthy’ neighbourhoods are. The AHAH index combines indicators under four different domains of accessibility:

* Retail environment (access to fast food outlets, pubs, tobacconists, gambling outlets),
    """
    test_summary = "AHAH is a dataset that talks about how unhealthy food can cause issues like diabetes."
    test_explanation = "The context does not provide information that mentions unhealthy food or diabetes."

    test_out = fix_chain.invoke(
        {
            "query": test_query,
            "context": test_context,
            "summary": test_summary,
            "explanation": test_explanation,
        }
    )
    print(test_out)
