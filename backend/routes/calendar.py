from flask import request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import os

# Google Calendar API Setup

SERVICE_ACCOUNT_FILE = "credential.json"
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    print("Error: credentials.json not found at", os.path.abspath(SERVICE_ACCOUNT_FILE))

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Load credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Initialize Calendar API
service = build("calendar", "v3", credentials=credentials)

# Your Google Calendar ID (Primary or Custom)
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")

def create_event(subject, start_time, end_time, description="Study Session"):
    """Create an event in Google Calendar."""
    event = {
        "summary": subject,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
    }
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event

def add_study_schedule():
    """Add study plan sessions to Google Calendar."""
    try:
        data = request.json
        daily_schedule = data.get("daily_schedule", [])

        if not daily_schedule:
            return jsonify({"error": "No study schedule found"}), 400

        events = []
        for day in daily_schedule:
            for session in day["subjects"]:
                # Convert start and end time to proper datetime format
                date = datetime.datetime.strptime(day["day"], "%A").date()
                start_datetime = datetime.datetime.combine(date, datetime.datetime.strptime(session["start_time"], "%I:%M %p").time())
                end_datetime = datetime.datetime.combine(date, datetime.datetime.strptime(session["end_time"], "%I:%M %p").time())

                # Convert to ISO format
                start_iso = start_datetime.isoformat()
                end_iso = end_datetime.isoformat()

                event = create_event(session["name"], start_iso, end_iso)
                events.append(event)

        return jsonify({"message": "Study schedule added to Google Calendar!", "events": events})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_study_schedule():
    """Retrieve upcoming study sessions from Google Calendar."""
    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"  # Get current time in ISO format
        events_result = (
            service.events()
            .list(calendarId=CALENDAR_ID, timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime")
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return jsonify({"message": "No upcoming study sessions found."})

        study_sessions = [
            {"subject": event["summary"], "start_time": event["start"]["dateTime"], "end_time": event["end"]["dateTime"]}
            for event in events
        ]

        return jsonify({"study_sessions": study_sessions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
