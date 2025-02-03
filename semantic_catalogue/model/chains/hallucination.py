from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from semantic_catalogue.common.settings import cfg

_ = load_dotenv()

human = """
You are grading text summaries of source documents focused on faithfulness and detection of any hallucinations.

Ensure that the Assistant's Summary meets the following criteria: 
(1) it does not contain information outside the score of the source document provided
(2) the summary should be fully grounded in and based upon the source documents

Score:
A score of 1 means that the Assistant Summary meets the criteria. This is the highest (best) score. 
A score of 0 means that the Assistant Summary does not the criteria. This is the lowest possible score you can give.

Explain your reasoning step-by-step to ensure your reasoning and conclusion are correct. 

Assistant's Summary: {generation}

Source document: {document}
"""


class HallucinationChecker(BaseModel):
    """Grade the summary based upon the above criteria."""

    score: int = Field(..., description="Score for the summary")
    explanation: str = Field(..., description="Explain your reasoning for the score")


llm = ChatOpenAI(model=cfg.model.llm, temperature=0)
SLLM = llm.with_structured_output(HallucinationChecker, strict=True)

hallucination_prompt = ChatPromptTemplate([("system", human)])
hallucination_grader_chain = hallucination_prompt | SLLM

if __name__ == "__main__":
    test_document = "Water is wet."
    test_generation = "Water is dry."

    test_out = hallucination_grader_chain.invoke(
        {"document": test_document, "generation": test_generation}
    )
    print(test_out)
