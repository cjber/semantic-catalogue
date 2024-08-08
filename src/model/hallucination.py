from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from src.common.settings import cfg
from src.model.grader import structured_llm_grader

_ = load_dotenv()


class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


llm = ChatOpenAI(model=cfg.model.llm, temperature=0)
structured_llm_grader = llm.with_structured_output(GradeHallucinations)

system = """
You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
Give a binary score 'yes' or 'no'. 'yes' means that the answer is grounded in / supported by the set of facts.
"""
hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Set of facts: \n\n {document} \n\n LLM generation: {generation}"),
    ]
)

hallucination_grader = hallucination_prompt | structured_llm_grader

hallucination_grader.invoke(
    {
        "document": "8",
        "generation": 'The dataset contains information on the top 8 most popular pizza toppings, which directly relates to the query for "pizza." Users interested in pizza preferences or trends may find this dataset relevant for ana lyzing popular topping choices. This dataset can provide insights into consumer preferences and help businesses i n the food industry make informed decisions regarding their pizza offerings.',
    }
)
