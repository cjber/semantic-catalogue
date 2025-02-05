from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from semantic_catalogue.model.llms.llm import LLM

human = """
A user has queried a data catalogue, which has returned a relevant dataset.

Explain the relevance of this dataset to the query in under three sentences. Use your own knowledge or the data profile. Do not say it is unrelated; attempt to find a relevant connection.

Query: "{query}"

Dataset description:

{context}
"""

gen_prompt = ChatPromptTemplate.from_messages([("human", human)])
rag_chain = gen_prompt | LLM | StrOutputParser()

if __name__ == "__main__":
    test_query = "healthy food"
    test_context = """
AHAH (the index of ‘Access to Healthy Assets and Hazards’) is a multi-dimensional index developed by the CDRC for Great Britain measuring how ‘healthy’ neighbourhoods are. The AHAH index combines indicators under four different domains of accessibility:

* Retail environment (access to fast food outlets, pubs, tobacconists, gambling outlets),
    """

    test_out = rag_chain.invoke({"query": test_query, "context": test_context})
    print(test_out)
