"""
Day 39 - Flight Sheet Data Manager
Manages destination cities, IATA airport codes, and target budget threshold prices.
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "flight_destinations.json")

DEFAULT_DESTINATIONS = [
    {"city": "Paris", "iataCode": "PAR", "lowestPrice": 54},
    {"city": "Frankfurt", "iataCode": "FRA", "lowestPrice": 42},
    {"city": "Tokyo", "iataCode": "TYO", "lowestPrice": 485},
    {"city": "Hong Kong", "iataCode": "HKG", "lowestPrice": 551},
    {"city": "Istanbul", "iataCode": "IST", "lowestPrice": 95},
    {"city": "Kuala Lumpur", "iataCode": "KUL", "lowestPrice": 414},
    {"city": "New York", "iataCode": "NYC", "lowestPrice": 240},
    {"city": "San Francisco", "iataCode": "SFO", "lowestPrice": 260},
    {"city": "Cape Town", "iataCode": "CPT", "lowestPrice": 378},
    {"city": "Sydney", "iataCode": "SYD", "lowestPrice": 599}
]


class DataManager:
    """Manages destination thresholds and airport codes."""

    def __init__(self):
        self.destinations = self.load_destinations()

    def load_destinations(self) -> list:
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        # Initialize default file
        self.save_destinations(DEFAULT_DESTINATIONS)
        return DEFAULT_DESTINATIONS

    def save_destinations(self, data: list):
        self.destinations = data
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add_destination(self, city: str, iata: str, target_price: float):
        self.destinations.append({"city": city, "iataCode": iata.upper(), "lowestPrice": target_price})
        self.save_destinations(self.destinations)
