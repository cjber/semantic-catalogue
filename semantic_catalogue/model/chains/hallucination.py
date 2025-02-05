from langchain import hub
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from semantic_catalogue.common.settings import cfg

prompt = hub.pull("cjber/hallucination-checker")


class HallucinationChecker(BaseModel):
    score: int = Field(..., description="Score for the summary.")
    explanation: str = Field(..., description="Explain your reasoning for the score.")


llm = ChatOpenAI(model=cfg.model.llm, temperature=0)
SLLM = llm.with_structured_output(HallucinationChecker, strict=True)

hallucination_grader_chain = prompt | SLLM

if __name__ == "__main__":
    test_document = "Water is wet."
    test_generation = "Water is dry."

    test_out = hallucination_grader_chain.invoke(
        {"document": test_document, "generation": test_generation}
    )
    print(test_out)
