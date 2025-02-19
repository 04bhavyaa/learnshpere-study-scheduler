import pickle
import numpy as np
from flask import jsonify
from utils.load_models import load_model
from flask import Blueprint, request, jsonify

# Load the trained model
study_predictor = load_model("artifacts/study_predictor.pkl")

# create blueprint
predictions_bp = Blueprint("predictions", __name__)

@predictions_bp.route("/predict_performance", methods=["POST"])
def predict_performance(data):
    try:
        features = np.array([
            data["gender"], data["education"], data["subject_mapping"], 
            data["absence_mapping"]
        ]).reshape(1, -1)
        
        prediction = study_predictor.predict(features)[0]
        return jsonify({"performance_level": prediction})

    except Exception as e:
        return jsonify({"error": str(e)})
