"""
Day 38 - Workout Tracking Engine
Integrates Nutritionix Natural Language Exercise API with Sheety REST Google Sheets API.
Includes offline natural language exercise heuristic parsing so workouts can be calculated
and logged locally without requiring paid API keys.
"""

import datetime as dt
import json
import os
import re
import sys
import urllib.request

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

LOCAL_WORKOUT_LOG = os.path.join(os.path.dirname(__file__), "workout_log.json")

# API Configuration (configurable via environment variables)
NUTRITIONIX_APP_ID = os.environ.get("NUTRITIONIX_APP_ID", "demo_nutritionix_id")
NUTRITIONIX_API_KEY = os.environ.get("NUTRITIONIX_API_KEY", "demo_nutritionix_key")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT", "https://api.sheety.co/demo_user/workoutTracking/workouts")
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN", "demo_bearer_token")

# Biometric baseline (configurable)
USER_WEIGHT_KG = float(os.environ.get("USER_WEIGHT_KG", "70.0"))
USER_HEIGHT_CM = float(os.environ.get("USER_HEIGHT_CM", "175.0"))
USER_AGE = int(os.environ.get("USER_AGE", "25"))


def parse_exercises_nlp(query_text: str) -> list:
    """
    Sends natural language query to Nutritionix API.
    Falls back to intelligent local heuristic parser if API is in demo mode or unreachable.
    """
    url = "https://trackapi.nutritionix.com/v2/natural/exercise"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "WorkoutTracker/1.0"
    }
    payload = {
        "query": query_text,
        "gender": "male",
        "weight_kg": USER_WEIGHT_KG,
        "height_cm": USER_HEIGHT_CM,
        "age": USER_AGE
    }

    if "demo" not in NUTRITIONIX_APP_ID:
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    return data.get("exercises", [])
        except Exception:
            pass

    # Intelligent Local Heuristic Parser (Offline Mode)
    # Extracts common exercises, durations, and estimates calories burned based on standard MET formulas
    exercises = []
    text_lower = query_text.lower()

    # MET values: Metabolic Equivalent of Task
    met_table = {
        "run": (10.0, "Running", 30),
        "jog": (8.0, "Jogging", 30),
        "walk": (3.8, "Walking", 30),
        "cycle": (8.5, "Cycling", 45),
        "bike": (8.5, "Cycling", 45),
        "swim": (8.0, "Swimming", 40),
        "yoga": (3.0, "Yoga", 30),
        "gym": (6.0, "Weightlifting", 45),
        "lift": (6.0, "Weightlifting", 45),
        "pushup": (5.0, "Calisthenics", 15),
        "squat": (5.0, "Calisthenics", 15)
    }

    found = False
    for keyword, (met, display_name, default_min) in met_table.items():
        if keyword in text_lower:
            found = True
            # Check if minutes or miles mentioned
            dur_match = re.search(rf"(\d+)\s*(?:min|minute|mins)", text_lower)
            duration = int(dur_match.group(1)) if dur_match else default_min
            # Calories burned = Duration(min) * (MET * 3.5 * weight_kg) / 200
            calories = round(duration * (met * 3.5 * USER_WEIGHT_KG) / 200, 1)
            exercises.append({
                "name": display_name,
                "duration_min": duration,
                "nf_calories": calories
            })

    if not found:
        # Generic cardio fallback
        exercises.append({
            "name": query_text.title(),
            "duration_min": 30,
            "nf_calories": round(30 * (6.0 * 3.5 * USER_WEIGHT_KG) / 200, 1)
        })

    return exercises


def log_workout_to_sheety(exercise_name: str, duration_min: float, calories: float) -> bool:
    """
    Posts workout record to Google Sheets via Sheety REST API.
    Also records to local workout_log.json database.
    """
    now = dt.datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%X")

    row_data = {
        "workout": {
            "date": date_str,
            "time": time_str,
            "exercise": exercise_name.title(),
            "duration": duration_min,
            "calories": calories
        }
    }

    # 1. Save locally
    history = []
    if os.path.exists(LOCAL_WORKOUT_LOG):
        try:
            with open(LOCAL_WORKOUT_LOG, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

    history.append(row_data["workout"])
    with open(LOCAL_WORKOUT_LOG, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

    # 2. Sheety Google Sheets Cloud Dispatch
    if "demo" in SHEETY_ENDPOINT:
        print(f" [Local Logged] {date_str} {time_str} | {exercise_name.title()} | {duration_min} mins | {calories} kcal")
        return True

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SHEETY_TOKEN}"
        }
        data_bytes = json.dumps(row_data).encode("utf-8")
        req = urllib.request.Request(SHEETY_ENDPOINT, data=data_bytes, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status in (200, 201):
                print(f"✅ Cloud Sync: Committed to Google Sheets successfully!")
                return True
    except Exception as e:
        print(f"ℹ️ Google Sheets Cloud API note: {e}")
    return True


def view_workout_history():
    """Prints formatted workout journal."""
    if not os.path.exists(LOCAL_WORKOUT_LOG):
        print("No workouts recorded yet.")
        return

    with open(LOCAL_WORKOUT_LOG, "r", encoding="utf-8") as f:
        entries = json.load(f)

    if not entries:
        print("Workout history is empty.")
        return

    print("\n" + "=" * 65)
    print(" 🏋️ LOGGED WORKOUT HISTORY")
    print("=" * 65)
    print(f" {'DATE':12s} | {'TIME':10s} | {'EXERCISE':16s} | {'DURATION':10s} | {'CALORIES'}")
    print("=" * 65)
    total_cal = 0
    total_min = 0
    for w in entries:
        print(f" {w['date']:12s} | {w['time']:10s} | {w['exercise']:16s} | {w['duration']} mins    | {w['calories']} kcal")
        total_cal += w['calories']
        total_min += w['duration']
    print("=" * 65)
    print(f" Total Logged: {len(entries)} workouts | {total_min} minutes | {total_cal:.1f} kcal burned 🔥\n")
