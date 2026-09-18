"""
Day 39 - Flight Search API Engine
Queries Amadeus / Tequila flight search APIs or executes realistic live market simulator.
"""

import datetime as dt
import os
import random
from flight_data import FlightData

AMADEUS_API_KEY = os.environ.get("AMADEUS_API_KEY", "demo_api_key")
AMADEUS_API_SECRET = os.environ.get("AMADEUS_API_SECRET", "demo_secret")

AIRLINES = ["British Airways", "Lufthansa", "Air France", "Emirates", "Virgin Atlantic", "Singapore Airlines"]


class FlightSearch:
    """Handles flight querying, IATA resolution, and fare comparisons."""

    def __init__(self, origin_city: str = "London", origin_iata: str = "LON"):
        self.origin_city = origin_city
        self.origin_iata = origin_iata

    def check_flights(self, destination_city: str, destination_iata: str, target_budget: float) -> FlightData:
        """
        Searches round-trip flights departing tomorrow and returning in 7-14 days.
        Simulates live market pricing algorithm with occasional bargain deal drops.
        """
        now = dt.datetime.now()
        out_date = (now + dt.timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")
        return_date = (now + dt.timedelta(days=random.randint(15, 28))).strftime("%Y-%m-%d")

        # Flight price engine: occasional super-deals below target budget
        variation = random.choice([0.75, 0.85, 0.95, 1.10, 1.25, 1.40])
        current_market_price = round(target_budget * variation, 2)
        stops = 0 if current_market_price < 300 else random.choice([0, 1])

        return FlightData(
            price=current_market_price,
            origin_city=self.origin_city,
            origin_airport=self.origin_iata,
            destination_city=destination_city,
            destination_airport=destination_iata,
            out_date=out_date,
            return_date=return_date,
            airline=random.choice(AIRLINES),
            stop_overs=stops
        )
