from langchain_openai import ChatOpenAI

from semantic_catalogue.common.settings import cfg

LLM = ChatOpenAI(model=cfg.model.llm, temperature=0)
