from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
from dotenv import load_dotenv

# Import routes
from routes.chatbot import chatbot_bp
from routes.study_plan import study_plan_bp
from routes.calendar import calendar_bp
from routes.predictions import predictions_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (for frontend integration)

# Register Blueprints (Modular Routes)
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
app.register_blueprint(study_plan_bp, url_prefix="/study_plan")
app.register_blueprint(calendar_bp, url_prefix="/calendar")
app.register_blueprint(predictions_bp, url_prefix="/predict")

@app.route("/", methods=["GET"])
def home():
    """Root route to check API status."""
    return jsonify({"message": "Study Assistant API is running!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
