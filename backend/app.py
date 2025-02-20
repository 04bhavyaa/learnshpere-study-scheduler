from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.score_prediction import predict_score
from routes.performance_prediction import predict_performance
from routes.study_plan import generate_study_plan
from routes.chatbot import ai_chatbot  # Import updated chatbot
#from routes.calendar import add_study_schedule, get_study_schedule

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the AI Study Assistant API!"})

@app.route('/predict', methods=['POST']) 
def predict(): 
    input_data = request.get_json()
    if not input_data: 
        return jsonify({"error": "No input data provided"}), 400 
    return predict_score(input_data)

@app.route('/performance', methods=['POST'])
def performance():
    data = request.json
    return predict_performance(data)

@app.route('/study_plan', methods=['POST'])
def study_plan():
    data = request.get_json()
    return generate_study_plan(data)

@app.route('/studyplan', methods=['POST'])
def studyplan():
    data = request.get_json()
    return generate_study_plan(data)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    return ai_chatbot()

@app.route('/calendar/add', methods=['POST'])
def add_calendar_event():
    return add_study_schedule()

@app.route('/calendar/get', methods=['GET'])
def get_calendar_events():
    return get_study_schedule()

if __name__ == '__main__':
    app.run(debug=True)
