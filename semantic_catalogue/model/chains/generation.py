from typing import List

from langchain import hub
from pydantic import BaseModel

from semantic_catalogue.model.llms.llm import LLM

prompt = hub.pull("cjber/generation-with-citations")


class CitedAnswer(BaseModel):
    generation: str
    citations: List[int]


SLLM = LLM.with_structured_output(CitedAnswer)

generation_chain = prompt | SLLM

if __name__ == "__main__":
    test_query = "healthy food"
    test_docs = [
        "Doc ID: [1]\n\nAHAH Index provides information regarding fast food locations.",
        "Doc ID: [2]\n\nThe index also talks about access to parks.",
    ]

    generation_chain.invoke({"query": test_query, "context": test_docs})
