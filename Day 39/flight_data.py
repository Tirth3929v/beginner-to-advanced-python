"""
Day 39 - Flight Data Model
Encapsulates structured itinerary information for flight deals.
"""


class FlightData:
    """Represents a round-trip flight deal itinerary."""

    def __init__(
        self,
        price: float,
        origin_city: str,
        origin_airport: str,
        destination_city: str,
        destination_airport: str,
        out_date: str,
        return_date: str,
        airline: str = "Global Airways",
        stop_overs: int = 0
    ):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.airline = airline
        self.stop_overs = stop_overs

    def __str__(self):
        stops = "Direct" if self.stop_overs == 0 else f"{self.stop_overs} Stop(s)"
        return (
            f"✈️ {self.origin_city} ({self.origin_airport}) ➔ {self.destination_city} ({self.destination_airport})\n"
            f"💰 Price: £{self.price:.2f} ({stops})\n"
            f"📅 Outbound: {self.out_date} | Return: {self.return_date}\n"
            f"🏢 Airline: {self.airline}"
        )
