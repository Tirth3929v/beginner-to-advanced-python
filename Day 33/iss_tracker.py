"""
Day 33 - International Space Station (ISS) Overhead & Orbital Tracker
Demonstrates REST APIs, requests module, json payloads, status codes,
sunrise-sunset calculations, and geospatial distance math.
"""

import datetime as dt
import math
import sys
import urllib.error
import urllib.request
import json

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Default Coordinates (New Delhi / Gujarat, India or customizable)
DEFAULT_MY_LAT = 23.0225  # Latitude
DEFAULT_MY_LONG = 72.5714  # Longitude

ISS_API_URL = "http://api.open-notify.org/iss-now.json"
SUNRISE_API_URL = "https://api.sunrise-sunset.org/json"


def fetch_json(url: str, timeout: int = 5) -> dict:
    """Helper to fetch JSON over HTTP using urllib without external dependency."""
    req = urllib.request.Request(url, headers={"User-Agent": "Python-ISS-Tracker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        if response.status == 200:
            return json.loads(response.read().decode("utf-8"))
        raise RuntimeError(f"HTTP Status {response.status}")


def get_iss_position() -> tuple:
    """
    Fetches real-time latitude and longitude of the International Space Station.
    Falls back to simulated orbital telemetry if network/API is unreachable.
    """
    try:
        data = fetch_json(ISS_API_URL, timeout=4)
        lat = float(data["iss_position"]["latitude"])
        lng = float(data["iss_position"]["longitude"])
        return lat, lng, False
    except Exception:
        # Simulated orbital coordinates near user for demonstration
        sim_lat = round(DEFAULT_MY_LAT + 1.84, 4)
        sim_lng = round(DEFAULT_MY_LONG - 2.15, 4)
        return sim_lat, sim_lng, True


def is_night(lat: float, lng: float) -> tuple:
    """
    Checks if it is currently dark at the given latitude and longitude
    using the sunrise-sunset.org API.
    """
    url = f"{SUNRISE_API_URL}?lat={lat}&lng={lng}&formatted=0"
    now_utc = dt.datetime.now(dt.timezone.utc)
    now_hour = now_utc.hour

    try:
        data = fetch_json(url, timeout=4)
        sunrise_iso = data["results"]["sunrise"]
        sunset_iso = data["results"]["sunset"]

        # Parse sunrise and sunset hours (UTC)
        sunrise_hour = int(sunrise_iso.split("T")[1].split(":")[0])
        sunset_hour = int(sunset_iso.split("T")[1].split(":")[0])

        is_dark = (now_hour >= sunset_hour) or (now_hour <= sunrise_hour)
        return is_dark, sunrise_hour, sunset_hour, False
    except Exception:
        # Fallback approximation: 18:00 UTC to 06:00 UTC
        is_dark = (now_hour >= 18) or (now_hour <= 6)
        return is_dark, 6, 18, True


def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two points on Earth using Haversine formula."""
    r = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r * c, 2)


def check_iss_overhead(my_lat: float = DEFAULT_MY_LAT, my_lng: float = DEFAULT_MY_LONG) -> dict:
    """
    Comprehensive orbital check:
    1. Gets ISS position
    2. Calculates distance to user
    3. Checks if within +/- 5 degrees
    4. Checks if it is currently night time
    """
    iss_lat, iss_lng, iss_sim = get_iss_position()
    dist_km = calculate_distance_km(my_lat, my_lng, iss_lat, iss_lng)

    lat_diff = abs(iss_lat - my_lat)
    lng_diff = abs(iss_lng - my_lng)
    is_close = lat_diff <= 5.0 and lng_diff <= 5.0

    is_dark, sunrise_h, sunset_h, sun_sim = is_night(my_lat, my_lng)
    is_visible = is_close and is_dark

    return {
        "user_lat": my_lat,
        "user_lng": my_lng,
        "iss_lat": iss_lat,
        "iss_lng": iss_lng,
        "distance_km": dist_km,
        "is_close": is_close,
        "is_dark": is_dark,
        "is_visible": is_visible,
        "sunrise_hour_utc": sunrise_h,
        "sunset_hour_utc": sunset_h,
        "simulated": iss_sim or sun_sim
    }
