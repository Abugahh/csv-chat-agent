import os
import dotenv
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
dotenv.load_dotenv()

# Ensure Google credentials are set (if needed for API authentication)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/Moraa/Downloads/flowing-digit-452913-t3-a975db7f9ff4.json"

def get_llm():
    """Initialize and return the Google Gemini LLM."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    return ChatGoogleGenerativeAI(model="gemini-1.5-pro-001")

def create_agent(csv_path, extra_tools=None):
    """Creates and returns a CSV agent with memory and optional extra tools."""
    llm = get_llm()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Create the agent with memory and optional extra tools
    agent = create_csv_agent(
        llm,
        csv_path,
        verbose=True,
        allow_dangerous_code=True,
        memory=memory,
        extra_tools=extra_tools if extra_tools else []
    )
    
    return agent
