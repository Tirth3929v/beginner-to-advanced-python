"""
Day 35 - SMS Weather Rain Alert Engine
Demonstrates API authentication with keys, environment variables,
weather condition code analysis (< 700), and Twilio SMS dispatch.
"""

import json
import os
import sys
import urllib.parse
import urllib.request

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# API Configuration (configurable via environment variables)
OWM_API_KEY = os.environ.get("OWM_API_KEY", "demo_api_key_placeholder")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "demo_twilio_sid")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "demo_auth_token")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE", "+1234567890")
RECIPIENT_PHONE = os.environ.get("MY_PHONE_NUMBER", "+919876543210")

# Default coordinates: Ahmedabad / Delhi, India
DEFAULT_LAT = 23.0225
DEFAULT_LON = 72.5714


def fetch_weather_forecast(lat: float = DEFAULT_LAT, lon: float = DEFAULT_LON) -> dict:
    """Fetches 5-day / 3-hour forecast from OpenWeatherMap API or returns realistic mock."""
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OWM_API_KEY}&cnt=4"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "RainAlert/1.0"})
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8"))
    except Exception:
        pass

    # Realistic simulated 12-hour hourly forecast (includes a rain event at hour 6 for testing)
    return {
        "city": {"name": "Ahmedabad", "country": "IN"},
        "list": [
            {"dt_txt": "12:00:00", "weather": [{"id": 800, "main": "Clear", "description": "clear sky"}], "main": {"temp": 305.15}},
            {"dt_txt": "15:00:00", "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds"}], "main": {"temp": 303.80}},
            {"dt_txt": "18:00:00", "weather": [{"id": 500, "main": "Rain", "description": "light rain"}], "main": {"temp": 298.15}},
            {"dt_txt": "21:00:00", "weather": [{"id": 502, "main": "Rain", "description": "heavy intensity rain"}], "main": {"temp": 295.20}}
        ]
    }


def send_sms_alert(message_body: str, to_number: str = RECIPIENT_PHONE) -> bool:
    """
    Dispatches SMS using Twilio REST API.
    If Twilio credentials are demo or placeholder, prints simulated SMS dispatch card.
    """
    if "demo" in TWILIO_ACCOUNT_SID or "placeholder" in TWILIO_AUTH_TOKEN:
        print("\n" + "—" * 60)
        print(" 📱 [SIMULATED SMS DISPATCH - TWILIO SAFE TEST MODE]")
        print(f" From: {TWILIO_PHONE}")
        print(f" To:   {to_number}")
        print("—" * 60)
        print(f" Body: {message_body}")
        print("—" * 60)
        print("✨ (In production, set TWILIO_ACCOUNT_SID & TWILIO_AUTH_TOKEN to send live)")
        return True

    # Live Twilio HTTP Basic Auth Dispatch
    twilio_url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = urllib.parse.urlencode({
        "From": TWILIO_PHONE,
        "To": to_number,
        "Body": message_body
    }).encode("utf-8")

    req = urllib.request.Request(twilio_url, data=data)
    import base64
    auth = base64.b64encode(f"{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}".encode("ascii")).decode("ascii")
    req.add_header("Authorization", f"Basic {auth}")

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status in (200, 201):
                print(f"✅ SMS successfully delivered to {to_number}!")
                return True
    except Exception as e:
        print(f"❌ Twilio dispatch failed: {e}")
    return False


def check_rain_and_alert(lat: float = DEFAULT_LAT, lon: float = DEFAULT_LON) -> bool:
    """
    Analyzes weather condition IDs across the next 12 hours.
    Weather code < 700 indicates rain/snow/storm:
      - 2xx: Thunderstorm
      - 3xx: Drizzle
      - 5xx: Rain
      - 6xx: Snow
    """
    data = fetch_weather_forecast(lat, lon)
    forecasts = data.get("list", [])
    city = data.get("city", {}).get("name", "Your Location")

    will_rain = False
    rain_reasons = []

    print("\n" + "=" * 65)
    print(f" 🌦️ 12-HOUR HOURLY RADAR FORECAST FOR {city.upper()}")
    print("=" * 65)
    print(f" {'TIME':10s} | {'CONDITION':16s} | {'ID':5s} | {'STATUS'}")
    print("=" * 65)

    for item in forecasts:
        time_str = item.get("dt_txt", "").split(" ")[-1][:5]
        weather = item.get("weather", [{}])[0]
        cond_id = weather.get("id", 800)
        desc = weather.get("description", "Unknown").title()

        status = "☀️ Clear/Cloudy"
        if cond_id < 700:
            will_rain = True
            status = "🌧️ PRECIPITATION"
            rain_reasons.append(f"{time_str} ({desc})")

        print(f" {time_str:10s} | {desc:16s} | {cond_id:5d} | {status}")

    print("=" * 65)

    if will_rain:
        print(f"\n🌧️ RAIN DETECTED! Precipitations expected at: {', '.join(rain_reasons)}")
        sms_text = f"🌧️ Weather Alert for {city}: Rain expected in the next 12 hours! Remember to bring an ☔ umbrella!"
        send_sms_alert(sms_text)
        return True
    else:
        print("\n☀️ No precipitation detected in the next 12 hours. Enjoy your day!\n")
        return False
