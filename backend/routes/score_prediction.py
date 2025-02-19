import pickle
import numpy as np
from flask import jsonify, Blueprint
from utils.load_models import load_model

# Load the trained model
best_model = load_model("artifacts/best_model.pkl")

# Create blueprint
predictions_bp = Blueprint("predictions", __name__)

@predictions_bp.route("/predict_score", methods=["POST"])
def predict_score(data):
    try:
        features = np.array([
            data["gender"], data["mother_job"], data["father_job"], 
            data["freetime"], data["absences"], data["G1"], data["G2"], 
            data["school_support"], data["family_support"], 
            data["extra_paid_class"], data["extracurricular"], 
            data["higher_edu"], data["romantic_rel"]
        ]).reshape(1, -1)
        
        prediction = best_model.predict(features)[0]
        return jsonify({"final_grade_prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)})
