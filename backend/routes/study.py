from flask import Blueprint, request, jsonify
import json
import ollama
import re
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LangChain Model (Llama3.2 via Ollama)
llm = Ollama(model="llama3.2")
memory = ConversationBufferWindowMemory(k=5, return_messages=True)

# Function to extract JSON from AI response
def extract_json_from_response(response_text):
    """ Extracts JSON content from AI response if extra text is present. """
    match = re.search(r'\{.*\}', response_text, re.DOTALL)  # Finds JSON within text
    return match.group(0) if match else None

# Function to analyze performance level
def analyze_performance(scores):
    avg_score = sum(scores.values()) / len(scores) if scores else 0
    if avg_score >= 80:
        return "High"
    elif avg_score >= 50:
        return "Medium"
    else:
        return "Low"

# Function to identify strengths & weaknesses
def evaluate_subjects(scores):
    strengths = [subject for subject, score in scores.items() if score >= 75]
    weaknesses = [subject for subject, score in scores.items() if score < 50]
    return strengths, weaknesses

# Function to generate study plan
def generate_study_plan():
    try:
        data = request.json
        goal_statement = data.get("goal_statement", "Improve grades within a set timeframe.")
        subjects = data.get("subjects", [])
        daily_hours = data.get("daily_hours", 2)
        scores = data.get("scores", {})  # User's self-reported subject scores

        # Analyze performance, strengths & weaknesses
        performance_level = analyze_performance(scores)
        strengths, weaknesses = evaluate_subjects(scores)

        # AI Prompt for study plan
        prompt = f"""
        A student wants to achieve the following goal: {goal_statement}.
        Their subjects: {subjects}, Daily Study Hours: {daily_hours}
        Performance Level: {performance_level}
        Strengths: {strengths}, Weaknesses: {weaknesses}

        Generate a structured JSON study plan with:
        - A daily study schedule (subjects + time allocated)
        - Personalized AI learning tips based on weaknesses
        - Study resources to improve weak subjects
        - A progress tracking system (To-Do List & Completion Bar)
        - Final recommendations for performance improvement

        IMPORTANT:
        - Your response **must be in valid JSON format**.
        - Do NOT include any additional text before or after the JSON.
        """

        # Get AI-generated study plan
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
        response_content = response.get("message", {}).get("content", "")

        # Extract JSON from response
        json_text = extract_json_from_response(response_content)
        if json_text:
            study_plan = json.loads(json_text)
            return jsonify({
                "performance_level": performance_level,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "study_plan": study_plan
            })

        return jsonify({"error": "AI response did not contain valid JSON"}), 500

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response from AI"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
