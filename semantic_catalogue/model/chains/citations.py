from typing import List

from langchain_core.documents import Document
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from semantic_catalogue.model.llms.llm import LLM

human = """
Objective: Given a user's query and the returned dataset, your task is to summarise the relevance of this dataset to the query. Use the provided dataset snippets to construct a concise summary of no more than three sentences.

Instructions:
1. Relevance: Ensure your summary clearly highlights how the dataset is relevant to the user's query. Avoid stating that it is unrelated; find a meaningful connection.
2. Citations: For every sentence, include citations directly after the relevant information. Use the format '[SOURCE_NUMBER]' (e.g., 'The Space Needle is in Seattle [1][2]'). You must incorporate *all* provided sources.
3. Query Context: Consider the query's intent when summarising the dataset's relevance.

Query: "{query}"

Dataset Snippets:
{context}
"""

prompt = ChatPromptTemplate.from_messages([("human", human)])


class CitedAnswer(BaseModel):
    """
    Answer the user question based only on the given sources, and cite the sources used.
    """

    generation: str = Field(
        ...,
        description="A dataset summary linking a users query with a dataset. For each sentence, add the relevant citation right after. Repeats are allowed. Use '[SOURCE_NUMBER]' for the citation (e.g. 'The Space Needle is in Seattle [1][2]'). You MUST use ALL citations.",
    )
    citations: List[int] = Field(
        ...,
        description="The integer IDs of the SPECIFIC sources which justify the summary.",
    )




TLLM = LLM.bind_tools([CitedAnswer], tool_choice="CitedAnswer")

output_parser = JsonOutputKeyToolsParser(key_name="CitedAnswer", first_tool_only=True)
citation_chain = prompt | TLLM | output_parser

if __name__ == "__main__":

    citation
