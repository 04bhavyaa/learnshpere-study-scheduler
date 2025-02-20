from flask import Blueprint, request, jsonify
import json
import ollama
import re
import pickle
import numpy as np
import os
from datetime import datetime, timedelta
from langchain_community.llms import Ollama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path constants
MODEL_PATH = 'artifacts/best_model.pkl'
PERFORMANCE_PREDICTOR_PATH = 'study_predict.py'

# Create blueprint
study_plan_api = Blueprint('study_plan_api', __name__)

# Load the predictive model
def load_model():
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Extract JSON from AI response
def extract_json_from_response(response_text):
    match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if match:
        try:
            json_text = match.group(0)
            json.loads(json_text)
            return json_text
        except json.JSONDecodeError:
            return None
    return None

# Subject categorization for better resource matching
def categorize_subjects(subjects):
    categories = {
        "STEM": ["Math", "Physics", "Chemistry", "Biology", "Computer Science", "IT", "Statistics"],
        "Languages": ["English", "French", "Spanish", "German", "Arabic", "Chinese", "Japanese"],
        "Humanities": ["History", "Geography", "Philosophy", "Economics", "Psychology", "Sociology"],
        "Arts": ["Art", "Music", "Drama", "Literature", "Design"],
        "Sciences": ["Geology", "Environmental Science", "Astronomy", "Health Science"]
    }
    
    categorized = {}
    for subject in subjects:
        for category, subj_list in categories.items():
            if subject in subj_list:
                categorized[subject] = category
                break
        if subject not in categorized:
            categorized[subject] = "Other"
            
    return categorized

# Predict future performance based on student profile
def predict_performance(student_data, model=None):
    if model is None:
        model = load_model()
        if model is None:
            return {
                "predicted_grade": "Unable to predict",
                "confidence": 0,
                "predicted_improvement": False
            }
    
    try:
        # Extract features needed for prediction
        features = {
            "gender": 1 if student_data.get("gender") == "Male" else 0,
            "education_level": 0 if student_data.get("education") == "lower" else 
                              (1 if student_data.get("education") == "middle" else 2),
            "absences": 0 if student_data.get("absence_mapping") == "low" else 
                       (1 if student_data.get("absence_mapping") == "medium" else 2),
            "freetime": student_data.get("freetime", 3),
            "school_support": 1 if student_data.get("school_support") == "yes" else 0,
            "family_support": 1 if student_data.get("family_support") == "yes" else 0,
            "paid_classes": 1 if student_data.get("extra_paid_class") == "yes" else 0,
            "extracurricular": 1 if student_data.get("extracurricular") == "yes" else 0,
            "romantic": 1 if student_data.get("romantic_rel") == "yes" else 0,
            "higher_edu_plans": 1 if student_data.get("higher_education") == "yes" else 0,
            "grade1": student_data.get("grade1", 0),
            "grade2": student_data.get("grade2", 0)
        }
        
        # Convert to format expected by model
        input_features = np.array([list(features.values())])
        
        # Make prediction
        prediction = model.predict(input_features)[0]
        prediction_proba = np.max(model.predict_proba(input_features)[0])
        
        # Determine if prediction shows improvement
        current_grade = student_data.get("grade2", 0)
        predicted_improvement = prediction > current_grade
        
        return {
            "predicted_grade": round(float(prediction), 1),
            "confidence": round(float(prediction_proba), 2),
            "predicted_improvement": predicted_improvement
        }
    except Exception as e:
        print(f"Prediction error: {e}")
        return {
            "predicted_grade": "Error in prediction",
            "confidence": 0,
            "predicted_improvement": False
        }

# Generate resource recommendations based on subject and education level
def generate_resources(subjects, education_level):
    # Base resource database
    resource_database = {
        # STEM Resources
        "Math": {
            "lower": [
                {"name": "Khan Academy Kids", "url": "https://learn.khanacademy.org/khan-academy-kids/", "type": "Interactive learning"},
                {"name": "Math Playground", "url": "https://www.mathplayground.com/", "type": "Games & practice"}
            ],
            "middle": [
                {"name": "Khan Academy", "url": "https://www.khanacademy.org/math", "type": "Video lessons"},
                {"name": "IXL Math", "url": "https://www.ixl.com/math", "type": "Practice problems"}
            ],
            "high": [
                {"name": "Brilliant", "url": "https://brilliant.org", "type": "Problem-based learning"},
                {"name": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/courses/mathematics/", "type": "Advanced courses"}
            ]
        },
        "IT": {
            "lower": [
                {"name": "Code.org", "url": "https://code.org/", "type": "Beginner coding"},
                {"name": "Scratch", "url": "https://scratch.mit.edu/", "type": "Visual programming"}
            ],
            "middle": [
                {"name": "Codecademy", "url": "https://www.codecademy.com", "type": "Interactive tutorials"},
                {"name": "Khan Academy Computing", "url": "https://www.khanacademy.org/computing", "type": "Video lessons"}
            ],
            "high": [
                {"name": "freeCodeCamp", "url": "https://www.freecodecamp.org", "type": "Project-based learning"},
                {"name": "CS50", "url": "https://cs50.harvard.edu/x/", "type": "University course"}
            ]
        },
        # Humanities Resources
        "History": {
            "lower": [
                {"name": "BBC Bitesize History", "url": "https://www.bbc.co.uk/bitesize/subjects/zk26n39", "type": "Interactive lessons"},
                {"name": "History for Kids", "url": "https://www.historyforkids.net/", "type": "Child-friendly resources"}
            ],
            "middle": [
                {"name": "Crash Course History", "url": "https://www.youtube.com/user/crashcourse", "type": "Video series"},
                {"name": "Khan Academy History", "url": "https://www.khanacademy.org/humanities/world-history", "type": "Structured courses"}
            ],
            "high": [
                {"name": "Yale Open Courses", "url": "https://oyc.yale.edu/history", "type": "University lectures"},
                {"name": "JSTOR", "url": "https://www.jstor.org/", "type": "Academic articles"}
            ]
        },
        # Science Resources
        "Geology": {
            "lower": [
                {"name": "National Geographic Kids", "url": "https://kids.nationalgeographic.com/science/topic/geology", "type": "Interactive content"},
                {"name": "Geology for Kids", "url": "https://www.ducksters.com/science/geology.php", "type": "Simplified explanations"}
            ],
            "middle": [
                {"name": "USGS Education", "url": "https://www.usgs.gov/educational-resources", "type": "Educational resources"},
                {"name": "Earth Science Week", "url": "https://www.earthsciweek.org/classroom-activities", "type": "Activities"}
            ],
            "high": [
                {"name": "MinDat", "url": "https://www.mindat.org", "type": "Mineral database"},
                {"name": "Geology.com", "url": "https://geology.com/", "type": "Advanced articles"}
            ]
        }
    }
    
    # Add more subjects as needed...
    
    # Default resources for subjects not in database
    default_resources = {
        "lower": [
            {"name": "Khan Academy", "url": "https://www.khanacademy.org", "type": "Video lessons"},
            {"name": "BBC Bitesize", "url": "https://www.bbc.co.uk/bitesize", "type": "Interactive learning"}
        ],
        "middle": [
            {"name": "Khan Academy", "url": "https://www.khanacademy.org", "type": "Video lessons"},
            {"name": "Quizlet", "url": "https://quizlet.com", "type": "Flashcards & quizzes"}
        ],
        "high": [
            {"name": "Khan Academy", "url": "https://www.khanacademy.org", "type": "Video lessons"},
            {"name": "EdX", "url": "https://www.edx.org", "type": "Online courses"}
        ]
    }
    
    resources = []
    for subject in subjects:
        if subject in resource_database:
            if education_level in resource_database[subject]:
                subject_resources = resource_database[subject][education_level]
            else:
                # Fallback to middle if exact level not found
                subject_resources = resource_database[subject].get("middle", default_resources[education_level])
        else:
            # Use default resources if subject not in database
            subject_resources = default_resources[education_level]
            
        resources.append({
            "subject": subject,
            "resources": subject_resources
        })
    
    return resources

# Generate study techniques based on student profile
def generate_study_techniques(student_data):
    # Base techniques
    base_techniques = {
        "lower": [
            {"name": "Visual Learning", "description": "Use pictures, videos, and colors to learn concepts"},
            {"name": "Game-Based Learning", "description": "Turn study materials into games or competitions"},
            {"name": "Storytelling", "description": "Learn facts and concepts through stories and narratives"},
            {"name": "Movement Learning", "description": "Incorporate physical movement while studying"}
        ],
        "middle": [
            {"name": "Mind Mapping", "description": "Create visual diagrams connecting related concepts"},
            {"name": "Flashcards", "description": "Use cards with questions on one side and answers on the other"},
            {"name": "Cornell Note-Taking", "description": "Organized note-taking with main points and summary"},
            {"name": "Group Study", "description": "Learn with peers through discussion and explanation"}
        ],
        "high": [
            {"name": "Spaced Repetition", "description": "Review material at increasing intervals for better retention"},
            {"name": "Active Recall", "description": "Test yourself on material rather than passively reviewing"},
            {"name": "Pomodoro Technique", "description": "25 minutes of focused study followed by 5-minute breaks"},
            {"name": "Feynman Technique", "description": "Explain concepts in simple terms to identify knowledge gaps"}
        ]
    }
    
    # Special case techniques
    special_techniques = {
        "limited_time": [
            {"name": "Pomodoro Technique", "description": "25 minutes of focused study followed by 5-minute breaks"},
            {"name": "80/20 Rule", "description": "Focus on the 20% of content that yields 80% of results"}
        ],
        "declining_grades": [
            {"name": "Retrieval Practice", "description": "Actively recall information rather than re-reading"},
            {"name": "Interleaving", "description": "Mix different subjects/topics rather than block studying"}
        ],
        "low_motivation": [
            {"name": "Reward System", "description": "Set up small rewards for completing study goals"},
            {"name": "Study Buddy", "description": "Partner with someone to maintain accountability"}
        ],
        "high_absence": [
            {"name": "Recorded Lectures", "description": "Ask for or find recordings of missed classes"},
            {"name": "Structured Self-Study", "description": "Create detailed plans for independent learning"}
        ]
    }
    
    # Extract profile information
    education_level = student_data.get("education", "middle").lower()
    freetime = student_data.get("freetime", 3)
    romantic = student_data.get("romantic_rel", "no") == "yes"
    extracurricular = student_data.get("extracurricular", "no") == "yes"
    absence_level = student_data.get("absence_mapping", "medium")
    grade1 = student_data.get("grade1", 10)
    grade2 = student_data.get("grade2", 10)
    
    # Select appropriate techniques
    selected_techniques = []
    
    # Add base techniques for education level
    if education_level in base_techniques:
        selected_techniques.extend(base_techniques[education_level][:2])
    else:
        selected_techniques.extend(base_techniques["middle"][:2])
    
    # Add special case techniques
    if freetime <= 2 or romantic or extracurricular:
        selected_techniques.extend(special_techniques["limited_time"])
    
    if grade2 < grade1:
        selected_techniques.extend(special_techniques["declining_grades"])
    
    if absence_level == "high":
        selected_techniques.extend(special_techniques["high_absence"])
    
    return selected_techniques[:4]  # Limit to 4 techniques

# Generate optimized study schedule based on student profile
def generate_optimized_schedule(student_data):
    # Extract relevant data
    selected_subjects = [subject for subject, mapped in student_data.get("subject_mapping", {}).items() if mapped == 1]
    education_level = student_data.get("education", "middle").lower()
    freetime = student_data.get("freetime", 3)
    romantic = student_data.get("romantic_rel", "no") == "yes"
    extracurricular = student_data.get("extracurricular", "no") == "yes"
    
    # Base available hours based on free time
    available_hours = {
        1: 5,   # Very limited free time
        2: 8,   # Limited free time
        3: 12,  # Moderate free time
        4: 16,  # Good amount of free time
        5: 20   # Lots of free time
    }.get(freetime, 10)
    
    # Adjust for other activities
    if romantic:
        available_hours -= 3
    if extracurricular:
        available_hours -= 4
    
    # Ensure minimum study time
    available_hours = max(available_hours, 5)
    
    # Session duration based on education level
    session_duration = {
        "lower": 30,    # 30 minutes
        "middle": 45,   # 45 minutes
        "high": 60      # 60 minutes
    }.get(education_level, 45)
    
    # Calculate total sessions per week (convert hours to minutes, then divide by session duration)
    total_sessions = (available_hours * 60) // session_duration
    
    # Ensure at least one session per subject
    sessions_per_subject = max(1, total_sessions // len(selected_subjects))
    
    # Distribution across days (study 5 days a week)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    study_days = days[:5] + ([] if sessions_per_subject * len(selected_subjects) <= 5 else [days[5]])
    
    # Generate schedule
    schedule = []
    session_count = 0
    subject_index = 0
    
    start_times = {
        "lower": ["15:30", "16:15", "17:00"],
        "middle": ["16:00", "17:00", "18:00"],
        "high": ["16:30", "17:45", "19:00"]
    }.get(education_level, ["16:00", "17:00", "18:00"])
    
    for day in days:
        day_schedule = {"day": day, "sessions": []}
        
        # Only add study sessions on study days
        if day in study_days:
            # Maximum 2-3 sessions per day based on education level
            max_sessions_per_day = 2 if education_level == "lower" else 3
            day_sessions = 0
            
            while day_sessions < max_sessions_per_day and session_count < sessions_per_subject * len(selected_subjects):
                subject = selected_subjects[subject_index % len(selected_subjects)]
                subject_index += 1
                
                # Calculate end time
                start_time = start_times[day_sessions]
                start_dt = datetime.strptime(start_time, "%H:%M")
                end_dt = start_dt + timedelta(minutes=session_duration)
                end_time = end_dt.strftime("%H:%M")
                
                # Create session
                session = {
                    "subject": subject,
                    "time_block": f"{start_time} - {end_time}",
                    "duration_minutes": session_duration,
                    "focus_area": get_focus_area(subject, day_sessions),
                    "study_technique": get_study_technique(subject, education_level)
                }
                
                day_schedule["sessions"].append(session)
                day_sessions += 1
                session_count += 1
        
        # Weekend review sessions
        if day == "Saturday" and day not in study_days:
            day_schedule["sessions"].append({
                "subject": "Weekly Review",
                "time_block": "10:00 - 11:30",
                "duration_minutes": 90,
                "focus_area": "Review all subjects",
                "study_technique": "Active Recall"
            })
        
        schedule.append(day_schedule)
    
    return schedule

# Helper function to get focus area for a subject
def get_focus_area(subject, session_index):
    focus_areas = {
        "Math": ["Problem solving", "Concept mastery", "Practice exercises"],
        "IT": ["Programming practice", "Theory and concepts", "Project work"],
        "History": ["Key events timeline", "Analysis of causes/effects", "Historical figures"],
        "Geology": ["Earth processes", "Mineral identification", "Geological formations"],
        "Physics": ["Formulas and equations", "Concept understanding", "Problem solving"],
        "Chemistry": ["Chemical reactions", "Formula memorization", "Lab concepts"],
        "Biology": ["Terminology", "Systems understanding", "Diagrams and visuals"],
        "English": ["Vocabulary building", "Grammar practice", "Reading comprehension"],
        "French": ["Vocabulary practice", "Grammar rules", "Conversation practice"],
        "Spanish": ["Vocabulary building", "Verb conjugation", "Listening practice"],
        "Geography": ["Map skills", "Regional characteristics", "Environmental systems"]
    }
    
    default_areas = ["Concept review", "Practice problems", "Note organization"]
    
    if subject in focus_areas:
        return focus_areas[subject][session_index % len(focus_areas[subject])]
    else:
        return default_areas[session_index % len(default_areas)]

# Helper function to get study technique for a subject
def get_study_technique(subject, education_level):
    techniques = {
        "lower": {
            "Math": "Visual practice with manipulatives",
            "History": "Storytelling and timelines",
            "Science": "Hands-on experiments"
        },
        "middle": {
            "Math": "Problem sets with increasing difficulty",
            "History": "Timeline creation and analysis",
            "Science": "Conceptual diagrams and summaries"
        },
        "high": {
            "Math": "Practice problems and theorem proofs",
            "History": "Document analysis and essay preparation",
            "Science": "Research papers and lab reports"
        }
    }
    
    # Categorize subjects
    science_subjects = ["Physics", "Chemistry", "Biology", "Geology"]
    math_subjects = ["Math", "Statistics"]
    history_subjects = ["History", "Geography", "Economics"]
    
    if subject in math_subjects:
        category = "Math"
    elif subject in history_subjects:
        category = "History"
    elif subject in science_subjects:
        category = "Science"
    else:
        category = "Other"
    
    if education_level in techniques and category in techniques[education_level]:
        return techniques[education_level][category]
    else:
        default_techniques = {
            "lower": "Visual learning with frequent breaks",
            "middle": "Cornell note-taking and flashcards",
            "high": "Spaced repetition and active recall"
        }
        return default_techniques.get(education_level, "Active learning techniques")

# Main endpoint for generating study plans
@study_plan_api.route('/generate', methods=['POST'])
def generate_study_plan():
    try:
        # Get request data
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ["subject_mapping"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Get selected subjects
        selected_subjects = [subject for subject, mapped in data.get("subject_mapping", {}).items() if mapped == 1]
        if not selected_subjects:
            return jsonify({"error": "No subjects selected"}), 400
        
        # Get prediction using model
        prediction = predict_performance(data)
        
        # Generate prompt for AI
        from prompt_generator import generate_student_profile_prompt
        prompt = generate_student_profile_prompt(data)
        
        # Get AI-generated study plan
        try:
            response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
            response_content = response.get("message", {}).get("content", "")
            
            # Extract and validate JSON
            json_text = extract_json_from_response(response_content)
            if not json_text:
                # AI failed to generate a valid plan, use our backup generators
                ai_failed = True
            else:
                ai_plan = json.loads(json_text)
                ai_failed = False
        except Exception as e:
            print(f"AI generation error: {e}")
            ai_failed = True
        
        # If AI generation failed, use our backup generators
        if ai_failed:
            # Generate a schedule
            schedule = generate_optimized_schedule(data)
            
            # Generate resources
            resources = generate_resources(selected_subjects, data.get("education", "middle").lower())
            
            # Generate study techniques
            techniques = generate_study_techniques(data)
            
            # Generate study plan
            # Compile backup study plan
            study_plan = {
                "student_profile_summary": {
                    "key_factors": [
                        f"Gender: {data.get('gender', 'Not specified')}",
                        f"Education level: {data.get('education', 'middle')}",
                        f"Free time: {data.get('freetime', 3)}/5",
                        f"Attendance: {data.get('absence_mapping', 'medium')} absence rate"
                    ],
                    "performance_trend": "improving" if data.get("grade2", 0) > data.get("grade1", 0) else "declining",
                    "performance_level": prediction.get("predicted_grade", "Unknown"),
                    "confidence": prediction.get("confidence", 0),
                    "predicted_improvement": prediction.get("predicted_improvement", False)
                },
                "schedule": schedule,
                "resources": resources,
                "study_techniques": techniques
            }
        else:
            study_plan = ai_plan
        
        return jsonify(study_plan), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500