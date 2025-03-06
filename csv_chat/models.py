import os
import dotenv
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory

dotenv.load_dotenv()  # Load environment variables from .env file

def get_llm():
    """Initialize and return the LLM model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    return ChatGoogleGenerativeAI(model="gemini-1.5-pro-001")

def create_agent(csv_path):
    """Creates and returns a CSV agent with memory."""
    llm = get_llm()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return create_csv_agent(llm, csv_path, verbose=True, allow_dangerous_code=True, memory=memory)
