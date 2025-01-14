from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from semantic_catalogue.common.settings import cfg

_ = load_dotenv()


class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


llm = ChatOpenAI(model=cfg.model.llm, temperature=0)
hallucination_grader = llm.with_structured_output(GradeHallucinations)

system = """
You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.

Give a binary score 'yes' or 'no'. 'yes' means that the answer is grounded in / supported by the set of facts.
"""
hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Set of facts: \n\n {document} \n\n LLM generation: {generation}"),
    ]
)

hallucination_grader_chain = hallucination_prompt | hallucination_grader

if __name__ == "__main__":
    test_document = "Water is wet."
    test_generation = "Water is dry."

    test_out = hallucination_grader_chain.invoke(
        {"document": test_document, "generation": test_generation}
    )
    print(test_out)
