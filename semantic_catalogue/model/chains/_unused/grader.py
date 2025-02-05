from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from semantic_catalogue.model.llms.llm import LLM


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the query, 'yes' or 'no'"
    )


SLLM = LLM.with_structured_output(GradeDocuments)
system = """
You are a grader assessing relevance of a retrieved document to a user query. \n 
It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
If the document contains keyword(s) or semantic meaning related to the user query, grade it as relevant. \n
Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the query.
"""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User query: {query}"),
    ]
)

grader_chain = grade_prompt | SLLM

if __name__ == "__main__":
    test_document = "Water is wet."
    test_query = "Where is the moon?"

    test_out = grader_chain.invoke({"document": test_document, "query": test_query})
    print(test_out)
