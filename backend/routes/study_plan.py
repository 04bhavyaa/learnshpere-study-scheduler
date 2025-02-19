from flask import Blueprint, request, jsonify
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from dotenv import load_dotenv
import ollama

# Load environment variables
load_dotenv()

# Create Blueprint for Study Plan
study_plan_bp = Blueprint("study_plan", __name__)

# Initialize LangChain Model (Llama3.2 via Ollama)
llm = Ollama(model="llama3.2")
memory = ConversationBufferWindowMemory(k=5, return_messages=True)

# Goal Statement Guide Template (to be shared with users)
GOAL_STATEMENT_TEMPLATE = {
    "description": "Your goal statement should be specific, measurable, and time-bound.",
    "examples": [
        "I want to improve my math skills and score at least 18/20 in the final exam within the next 3 months. I will dedicate 2 hours daily.",
        "I aim to enhance my understanding of Science and History for better university applications. I will study 3 subjects daily and take weekly practice tests.",
        "I need to prepare for college entrance exams with a structured plan focusing on weak areas."
    ],
    "structure": {
        "goal": "What do you want to achieve?",
        "timeframe": "By when do you want to achieve it?",
        "study_hours": "How many hours per day will you dedicate?",
        "subjects": "Which subjects need more focus?"
    }
}

# LangChain Prompt for Study Plan
study_plan_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a study planner AI. Generate a structured study plan in JSON format based on user input."),
    ("user", "Subjects: {subjects}, Daily Study Hours: {daily_hours}, Start Date: {start_date}")
])

llm_chain = LLMChain(llm=llm, prompt=study_plan_prompt, memory=memory)

@study_plan_bp.route("/generate_plan", methods=["POST"])
def generate_study_plan(data):
    try:
        goal_statement = data.get("goal_statement", "Improve grades within a set timeframe.")
        final_grade = data.get("final_grade_prediction", 0)
        performance = data.get("performance_level", "unknown")

        # AI prompt to generate a structured study plan
        prompt = f"""
        A student is preparing to achieve the following goal: {goal_statement}.
        Predicted Final Grade: {final_grade}, Performance Level: {performance}.
        
        Generate a structured **JSON study schedule** with:
        - A **daily schedule** (subjects + time allocated)
        - **AI learning tips** for motivation
        - **Study resources** for better understanding
        - A **progress tracking system** (To-Do List & Completion Bar)
        
        The response **must be in JSON format**.
        """

        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
        study_plan = json.loads(response['message']['content'])  # Convert response to JSON

        return jsonify({"study_plan": study_plan})

    except Exception as e:
        return jsonify({"error": str(e)})
