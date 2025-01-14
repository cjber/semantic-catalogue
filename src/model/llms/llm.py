from langchain_openai import ChatOpenAI

from src.common.settings import cfg

LLM = ChatOpenAI(model=cfg.model.llm, temperature=0)
