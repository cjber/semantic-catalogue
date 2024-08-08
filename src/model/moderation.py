from dotenv import load_dotenv
from langchain.chains import OpenAIModerationChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

_ = load_dotenv()


OpenAIModerationChain._openai_pre_1_0 = False  # bug
moderate = OpenAIModerationChain()
