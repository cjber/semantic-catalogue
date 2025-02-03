from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from semantic_catalogue.model.llms.llm import LLM

human = """
The following is a users 'query', a retrieved 'context' taken from a document that relates to the query, and an **incorrect** 'summary' of the context with respect to the 'query'. Your job is to generate a **correct** summary based solely on the 'context', considering how it relates to the users 'query', avoiding any errors highlighted in the explanation.

- **Query**:
{query}

- **Incorrect Summary**:
{summary}

- **Explanation of Errors**:
{explanation}

- **Original Context**:
{context}

**Your task**: Write a concise and accurate summary of the original context, taking into account the errors highlighted in the explanation. You must consider how the 'query' relates with this new summary.
"""

gen_prompt = ChatPromptTemplate.from_messages([("human", human)])
fix_chain = gen_prompt | LLM | StrOutputParser()

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
