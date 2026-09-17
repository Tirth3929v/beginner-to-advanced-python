"""
Day 85: Typing Speed Test Engine & WPM Benchmark
Calculates Net WPM, Gross WPM, accuracy %, and character error diffs.
"""

import time
import random
from typing import Dict, List, Tuple


SAMPLE_PASSAGES = [
    (
        "Python is an interpreted, high-level, general-purpose programming language. "
        "Its design philosophy emphasizes code readability with the use of significant indentation. "
        "Language constructs and an object-oriented approach aim to help programmers write clear, logical code."
    ),
    (
        "Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex. "
        "Complex is better than complicated. Flat is better than nested. Sparse is better than dense. "
        "Readability counts. Special cases aren't special enough to break the rules."
    ),
    (
        "Computer science is no more about computers than astronomy is about telescopes. "
        "The question of whether machines can think is about as relevant as the question of whether submarines can swim. "
        "Simplicity is prerequisite for reliability."
    ),
    (
        "First, solve the problem. Then, write the code. Any fool can write code that a computer can understand. "
        "Good programmers write code that humans can understand. Make it work, make it right, make it fast."
    )
]


class TypingSpeedTest:
    def __init__(self, passage: str = None):
        self.target_text = passage if passage else random.choice(SAMPLE_PASSAGES)
        self.start_time: float = 0.0
        self.end_time: float = 0.0

    def start(self):
        self.start_time = time.time()

    def finish(self, user_text: str) -> Dict[str, float]:
        self.end_time = time.time()
        elapsed_seconds = max(0.5, self.end_time - self.start_time)
        return self.calculate_metrics(user_text, elapsed_seconds)

    def calculate_metrics(self, user_text: str, elapsed_seconds: float) -> Dict[str, float]:
        minutes = elapsed_seconds / 60.0

        # Character comparisons
        target_len = len(self.target_text)
        user_len = len(user_text)

        correct_chars = 0
        min_len = min(target_len, user_len)
        for i in range(min_len):
            if self.target_text[i] == user_text[i]:
                correct_chars += 1

        errors = abs(target_len - user_len) + (min_len - correct_chars)

        # Standard typing metrics (5 characters = 1 standard word)
        gross_wpm = (user_len / 5.0) / minutes if minutes > 0 else 0.0
        net_wpm = max(0.0, ((user_len - errors) / 5.0) / minutes) if minutes > 0 else 0.0
        accuracy = (correct_chars / max(1, user_len)) * 100.0

        # Performance tier
        tier = "Beginner (<30 WPM)"
        if net_wpm >= 90:
            tier = "Pro / Master (90+ WPM) 🏆"
        elif net_wpm >= 70:
            tier = "Fast Typist (70-90 WPM) ⚡"
        elif net_wpm >= 50:
            tier = "Fluent (50-70 WPM) 👍"
        elif net_wpm >= 30:
            tier = "Average (30-50 WPM) 📝"

        return {
            "elapsed_seconds": round(elapsed_seconds, 2),
            "gross_wpm": round(gross_wpm, 1),
            "net_wpm": round(net_wpm, 1),
            "accuracy_pct": round(accuracy, 1),
            "total_typed_chars": user_len,
            "correct_chars": correct_chars,
            "errors": errors,
            "tier": tier
        }
