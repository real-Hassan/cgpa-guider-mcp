from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_MODEL = "groq:openai/gpt-oss-20b"

llm = init_chat_model(
    GROQ_MODEL, 
    api_key=os.getenv("GROQ_API_KEY"),
    reasoning_format="parsed")
