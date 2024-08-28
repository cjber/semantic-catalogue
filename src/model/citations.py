from typing import List

from dotenv import load_dotenv
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from src.common.settings import cfg

load_dotenv()

llm = ChatOpenAI(model=cfg.model.llm, temperature=0)
human = """
A user has queried a data catalogue, which has returned a relevant dataset.

Summarise the relevance of this dataset to the query in under three sentences, using the source snippets provided. Do not say it is unrelated; find a relevant connection. For each sentence, a the relevant citation right after. Repeats are allowed. Use '[SOURCE_NUMBER]' for the citation (e.g. 'The Space Needle is in Seattle [1][2]'). You MUST use ALL citations.

Query: "{query}"

Dataset snippets:

{context}
"""

prompt = ChatPromptTemplate.from_messages([("human", human)])


class CitedAnswer(BaseModel):
    """
    Answer the user question based only on the given sources, and cite the sources used.
    """

    generation: str = Field(
        ...,
        description="A dataset summary linking a users query with a dataset. For each sentence, a the relevant citation right after. Repeats are allowed. Use '[SOURCE_NUMBER]' for the citation (e.g. 'The Space Needle is in Seattle [1][2]'). You MUST use ALL citations.",
    )
    citations: List[int] = Field(
        ...,
        description="The integer IDs of the SPECIFIC sources which justify the summary.",
    )


def format_docs_with_id(docs: List[Document]) -> str:
    formatted = [
        f"Source ID: {i}\nArticle Title: {doc.metadata['title']}\nArticle Snippet: {doc.page_content}"
        for i, doc in enumerate(docs)
    ]
    return "\n\n" + "\n\n".join(formatted)


llm_with_tool = llm.bind_tools([CitedAnswer], tool_choice="CitedAnswer")

output_parser = JsonOutputKeyToolsParser(key_name="CitedAnswer", first_tool_only=True)
answer_citations = prompt | llm_with_tool | output_parser
