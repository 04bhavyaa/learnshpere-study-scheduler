import numpy as np
import pandas as pd
from flask import jsonify
from utils.load_models import load_model

# Load models once
best_model = load_model("artifacts/best_model.pkl")
preprocess = load_model("artifacts/preprocess.pkl")

# Define the function
def predict_score(input_data):
    required_keys = [
        "gender", "mother_job", "father_job", "freetime",
        "absences", "grade_1", "grade_2",
        "school_support", "family_support", "extra_paid_class",
        "extracurricular", "higher_edu", "romantic_rel", "education"
    ]
    
    subject_keys = [
        "IT", "French", "Arabic", "Science", "English", "Biology", 
        "Spanish", "Chemistry", "Geology", "Math", "History"
    ]

    # Ensure all required keys are present
    missing_keys = [key for key in required_keys if key not in input_data]
    
    if "subjects" not in input_data:
        missing_keys.extend(subject_keys)  # Add missing subject keys

    if missing_keys:
        return jsonify({"error": f"Missing keys: {', '.join(missing_keys)}"}), 400

    try:
        # Convert categorical absences (if needed)
        absences_map = {"low": 0, "medium": 1, "high": 2}
        if input_data["absences"] in absences_map:
            input_data["absences"] = absences_map[input_data["absences"]]

        # Expand subjects into separate features
        subjects = input_data.pop("subjects", {})
        for subject in subject_keys:
            input_data[subject] = subjects.get(subject, 0)  # Default to 0 if missing

        # Convert input_data to DataFrame
        input_df = pd.DataFrame([input_data])

        # Preprocess input
        features_transformed = preprocess.transform(input_df)

        # Predict
        prediction = best_model.predict(features_transformed)[0]

        return jsonify({"final_grade_prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
