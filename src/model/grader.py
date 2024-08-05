from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from src.common.settings import cfg

_ = load_dotenv()


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the query, 'yes' or 'no'"
    )


llm = ChatOpenAI(model=cfg.model.llm, temperature=0)
structured_llm_grader = llm.with_structured_output(GradeDocuments)
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

retrieval_grader = grade_prompt | structured_llm_grader
