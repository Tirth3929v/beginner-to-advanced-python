"""
Day 37 - Pixela Habit Tracking Engine
Demonstrates HTTP request methods (POST, PUT, DELETE), custom HTTP headers (X-USER-TOKEN),
querying APIs, and rendering local terminal GitHub-style habit commit heatmaps.
"""

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PIXELA_ENDPOINT = "https://pixe.la/v1/users"
LOCAL_STORAGE = os.path.join(os.path.dirname(__file__), "habit_log.json")

# Default User Credentials (can be overridden with environment variables)
DEFAULT_USERNAME = os.environ.get("PIXELA_USERNAME", "my_pixela_username")
DEFAULT_TOKEN = os.environ.get("PIXELA_TOKEN", "your_pixela_token_here")
DEFAULT_GRAPH_ID = "graph1"


# ------------------------------------------------------------------------------
# 1. LOCAL STORAGE & OFFLINE HEATMAP CACHE
# ------------------------------------------------------------------------------

def load_local_habits() -> dict:
    if os.path.exists(LOCAL_STORAGE):
        try:
            with open(LOCAL_STORAGE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_local_habit(date_str: str, quantity: float, unit: str = "hours"):
    data = load_local_habits()
    data[date_str] = {"quantity": quantity, "unit": unit}
    with open(LOCAL_STORAGE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ------------------------------------------------------------------------------
# 2. HTTP REQUEST DISPATCHER (POST, PUT, DELETE)
# ------------------------------------------------------------------------------

def make_pixela_request(url: str, method: str, body: dict = None, token: str = DEFAULT_TOKEN) -> dict:
    """Executes HTTP requests with custom headers and method overrides."""
    headers = {
        "User-Agent": "PixelaTracker/1.0",
        "X-USER-TOKEN": token,
        "Content-Type": "application/json"
    }
    data_bytes = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = response.read().decode("utf-8")
            return json.loads(res_data) if res_data else {"isSuccess": True}
    except urllib.error.HTTPError as http_err:
        try:
            err_payload = json.loads(http_err.read().decode("utf-8"))
            return err_payload
        except Exception:
            return {"isSuccess": False, "message": str(http_err)}
    except Exception as e:
        return {"isSuccess": False, "message": str(e)}


# ------------------------------------------------------------------------------
# 3. CORE HABIT TRACKING OPERATIONS
# ------------------------------------------------------------------------------

def create_user(username: str = DEFAULT_USERNAME, token: str = DEFAULT_TOKEN) -> dict:
    """POST: https://pixe.la/v1/users"""
    payload = {
        "token": token,
        "username": username,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }
    print(f"\n🚀 Creating Pixela user account: '{username}'...")
    res = make_pixela_request(PIXELA_ENDPOINT, method="POST", body=payload, token=token)
    print(f"Result: {res.get('message', 'No response')}")
    return res


def create_graph(username: str = DEFAULT_USERNAME, token: str = DEFAULT_TOKEN, graph_id: str = DEFAULT_GRAPH_ID, name: str = "Coding Habit") -> dict:
    """POST: https://pixe.la/v1/users/<username>/graphs"""
    endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs"
    payload = {
        "id": graph_id,
        "name": name,
        "unit": "hours",
        "type": "float",
        "color": "shibafu"  # Green
    }
    print(f"\n📊 Initializing graph '{graph_id}' ({name})...")
    res = make_pixela_request(endpoint, method="POST", body=payload, token=token)
    print(f"Result: {res.get('message', 'No response')}")
    return res


def log_habit_pixel(quantity: float, date_str: str = None, username: str = DEFAULT_USERNAME, graph_id: str = DEFAULT_GRAPH_ID, token: str = DEFAULT_TOKEN) -> dict:
    """POST: https://pixe.la/v1/users/<username>/graphs/<graph_id>"""
    if not date_str:
        date_str = dt.datetime.now().strftime("%Y%m%d")

    endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs/{graph_id}"
    payload = {
        "date": date_str,
        "quantity": str(quantity)
    }

    print(f"\n🟩 Posting {quantity} units to Pixela for date {date_str}...")
    res = make_pixela_request(endpoint, method="POST", body=payload, token=token)

    # Save to local cache regardless of network
    save_local_habit(date_str, quantity, "hours")
    print(f"Result: {res.get('message', 'Committed to local & cloud database.')}")
    return res


def update_habit_pixel(quantity: float, date_str: str, username: str = DEFAULT_USERNAME, graph_id: str = DEFAULT_GRAPH_ID, token: str = DEFAULT_TOKEN) -> dict:
    """PUT: https://pixe.la/v1/users/<username>/graphs/<graph_id>/<yyyyMMdd>"""
    endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs/{graph_id}/{date_str}"
    payload = {"quantity": str(quantity)}

    print(f"\n✏️ Updating habit record on {date_str} to {quantity} units (HTTP PUT)...")
    res = make_pixela_request(endpoint, method="PUT", body=payload, token=token)
    save_local_habit(date_str, quantity, "hours")
    print(f"Result: {res.get('message', 'Updated successfully.')}")
    return res


def delete_habit_pixel(date_str: str, username: str = DEFAULT_USERNAME, graph_id: str = DEFAULT_GRAPH_ID, token: str = DEFAULT_TOKEN) -> dict:
    """DELETE: https://pixe.la/v1/users/<username>/graphs/<graph_id>/<yyyyMMdd>"""
    endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs/{graph_id}/{date_str}"
    print(f"\n🗑️ Deleting habit record on {date_str} (HTTP DELETE)...")
    res = make_pixela_request(endpoint, method="DELETE", token=token)

    # Remove from local cache
    data = load_local_habits()
    if date_str in data:
        del data[date_str]
        with open(LOCAL_STORAGE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    print(f"Result: {res.get('message', 'Deleted successfully.')}")
    return res


def print_terminal_heatmap():
    """Renders an ASCII GitHub-style commitment heatmap from recorded days."""
    habits = load_local_habits()
    print("\n" + "=" * 65)
    print(" 🟩 HABIT COMMITMENT HEATMAP (PAST 14 DAYS)")
    print("=" * 65)

    today = dt.datetime.now()
    dates = [(today - dt.timedelta(days=i)).strftime("%Y%m%d") for i in range(13, -1, -1)]

    # Heatmap visual symbols
    tiles = []
    for d in dates:
        qty = habits.get(d, {}).get("quantity", 0)
        if qty <= 0:
            tiles.append("⬜")  # 0 hours
        elif qty < 2.0:
            tiles.append("🟨")  # Light progress
        elif qty < 4.0:
            tiles.append("🟩")  # Solid progress
        else:
            tiles.append("🔥")  # High intensity!

    print(" " + " ".join(tiles))
    print(" " + " ".join([d[4:6] + "/" + d[6:8] for d in dates]))
    print("=" * 65)
    print(" Legend: ⬜ 0 hrs | 🟨 0-2 hrs | 🟩 2-4 hrs | 🔥 4+ hrs")
    print(f" Cloud Pixela Web Graph URL: https://pixe.la/v1/users/{DEFAULT_USERNAME}/graphs/{DEFAULT_GRAPH_ID}.html\n")
