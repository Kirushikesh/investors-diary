import os
from dotenv import load_dotenv
from config.config import LANGCHAIN_TRACING_V2, LANGCHAIN_ENDPOINT, LANGCHAIN_PROJECT

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT