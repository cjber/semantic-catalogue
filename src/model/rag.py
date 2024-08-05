from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.common.settings import cfg

_ = load_dotenv()
human = """
A user has queried a data catalogue, which has returned a relevant dataset.

Explain the relevance of this dataset to the query in under three sentences. Use your own knowledge or the data profile. Do not say it is unrelated; attempt to find a relevant connection.

Query: "{query}"

Dataset description:

{context}
"""

gen_prompt = ChatPromptTemplate.from_messages([("human", human)])
llm = ChatOpenAI(model=cfg.model.llm, temperature=0)
rag_chain = gen_prompt | llm | StrOutputParser()
