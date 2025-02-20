from flask import Blueprint, request, jsonify
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import ollama
import re

# Load environment variables
load_dotenv()

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

# Updated approach using RunnableSequence (new LangChain standard)
study_plan_chain = study_plan_prompt | llm

def extract_json_from_response(response_text):
    """ Extracts JSON content from AI response if extra text is present. """
    match = re.search(r'\{.*\}', response_text, re.DOTALL)  # Finds JSON within text
    if match:
        return match.group(0)  # Extracts JSON part
    return None

def generate_study_plan(data):
    try:
        goal_statement = data.get("goal_statement", "Improve grades within a set timeframe.")

        # AI prompt to generate a structured study plan
        prompt = f"""
        A student is preparing to achieve the following goal: {goal_statement}.

        Generate a structured JSON study plan with:
        - A daily schedule (subjects + time allocated)
        - AI learning tips for motivation
        - Study resources for better understanding
        - A progress tracking system (To-Do List & Completion Bar)

        IMPORTANT: 
        - Your response **must be in valid JSON format**.
        - Do NOT include any additional text before or after the JSON.
        """

        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])

        # Extract response message content
        response_content = response.get("message", {}).get("content", "")

        # Try extracting JSON from the response
        json_text = extract_json_from_response(response_content)
        if json_text:
            study_plan = json.loads(json_text)  # Convert response to JSON
            return jsonify({"study_plan": study_plan})

        return jsonify({"error": "AI response did not contain valid JSON"}), 500

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response from AI"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
from flask import Blueprint, request, jsonify
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import ollama
import re

# Load environment variables
load_dotenv()

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

# Updated approach using RunnableSequence (new LangChain standard)
study_plan_chain = study_plan_prompt | llm

def extract_json_from_response(response_text):
    """ Extracts JSON content from AI response if extra text is present. """
    match = re.search(r'\{.*\}', response_text, re.DOTALL)  # Finds JSON within text
    if match:
        return match.group(0)  # Extracts JSON part
    return None

def generate_study_plan(data):
    try:
        goal_statement = data.get("goal_statement", "Improve grades within a set timeframe.")

        # AI prompt to generate a structured study plan
        prompt = f"""
        A student is preparing to achieve the following goal: {goal_statement}.

        Generate a structured JSON study plan with:
        - A daily schedule (subjects + time allocated)
        - AI learning tips for motivation
        - Study resources for better understanding
        - A progress tracking system (To-Do List & Completion Bar)

        IMPORTANT: 
        - Your response **must be in valid JSON format**.
        - Do NOT include any additional text before or after the JSON.
        """

        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])

        # Extract response message content
        response_content = response.get("message", {}).get("content", "")

        # Try extracting JSON from the response
        json_text = extract_json_from_response(response_content)
        if json_text:
            study_plan = json.loads(json_text)  # Convert response to JSON
            return jsonify({"study_plan": study_plan})

        return jsonify({"error": "AI response did not contain valid JSON"}), 500

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response from AI"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
