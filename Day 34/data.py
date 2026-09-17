"""
Day 34 - Open Trivia DB API Data Provider
Fetches 10 fresh boolean questions from the Open Trivia API.
Includes offline fallback questions in case of network unavailability.
"""

import json
import urllib.request
import urllib.error

TRIVIA_API_URL = "https://opentdb.com/api.php?amount=10&type=boolean"

FALLBACK_QUESTIONS = [
    {"question": "A slug's blood is green.", "correct_answer": "True"},
    {"question": "The loudest animal is the African Elephant.", "correct_answer": "False"},
    {"question": "Approximately one quarter of human bones are in the feet.", "correct_answer": "True"},
    {"question": "The total surface area of two human lungs is approximately 70 square meters.", "correct_answer": "True"},
    {"question": "In West Virginia, USA, if you accidentally hit an animal with your car, you are free to take it home to eat.", "correct_answer": "True"},
    {"question": "In London, UK, if you happen to die in the House of Parliament, you are technically entitled to a state funeral.", "correct_answer": "False"},
    {"question": "It is illegal to pee in the Ocean in Portugal.", "correct_answer": "True"},
    {"question": "You can lead a cow down stairs but not up stairs.", "correct_answer": "False"},
    {"question": "Google was originally called 'Backrub'.", "correct_answer": "True"},
    {"question": "Buzz Aldrin's mother's maiden name was 'Moon'.", "correct_answer": "True"}
]


def fetch_quiz_questions() -> list:
    """Fetches trivia questions from Open Trivia DB API or returns fallback deck."""
    try:
        req = urllib.request.Request(TRIVIA_API_URL, headers={"User-Agent": "QuizzerApp/1.0"})
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status == 200:
                payload = json.loads(response.read().decode("utf-8"))
                results = payload.get("results", [])
                if results:
                    return results
    except Exception:
        pass
    return FALLBACK_QUESTIONS
