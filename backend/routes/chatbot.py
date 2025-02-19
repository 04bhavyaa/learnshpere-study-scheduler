from flask import Blueprint, request, jsonify
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Blueprint for Chatbot
chatbot_bp = Blueprint("chatbot", __name__)

# Enable LangSmith Tracing
os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

# Initialize Llama3.2 Model (Ollama)
llm = Ollama(model="llama3.2")

# Initialize Memory for storing the last 5 messages
memory = ConversationBufferWindowMemory(k=5, return_messages=True)

# Define Chat Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI tutor. Answer students' study-related queries."),
    ("user", "{question}")
])

# Define Conversation Chain
chain = ConversationChain(llm=llm, memory=memory)

@chatbot_bp.route("/ai_chatbot", methods=["POST"])
def ai_chatbot():
    """Handles chatbot requests via API."""
    try:
        data = request.json
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400

        # Run conversation with memory
        response = chain.run(query)

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
