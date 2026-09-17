"""
Day 64: Movie Search Service
Handles movie metadata lookups using TMDB REST API with offline fallback catalog.
"""

import os
import requests
from typing import List, Dict, Any

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "your_tmdb_api_key_here")
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

FALLBACK_MOVIES = [
    {
        "id": 603,
        "title": "The Matrix",
        "year": 1999,
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "img_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
    },
    {
        "id": 157336,
        "title": "Interstellar",
        "year": 2014,
        "description": "The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel.",
        "img_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
    },
    {
        "id": 27205,
        "title": "Inception",
        "year": 2010,
        "description": "Cobb steals information from his targets by entering their dreams. He is wanted for his alleged role in his wife's murder.",
        "img_url": "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg"
    },
    {
        "id": 155,
        "title": "The Dark Knight",
        "year": 2008,
        "description": "Batman raises the stakes in his war on crime. With the help of allies Lt. Jim Gordon and DA Harvey Dent, Batman sets out to dismantle the remaining criminal organizations.",
        "img_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
    },
    {
        "id": 129,
        "title": "Spirited Away",
        "year": 2001,
        "description": "A young girl, Chihiro, becomes trapped in a strange new world of spirits. When her parents undergo a mysterious transformation, she must call upon courage she never knew she had.",
        "img_url": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg"
    }
]


def search_movies(query: str) -> List[Dict[str, Any]]:
    """Searches TMDB API or falls back to curated offline catalog."""
    if TMDB_API_KEY != "your_tmdb_api_key_here":
        try:
            params = {"api_key": TMDB_API_KEY, "query": query}
            response = requests.get(TMDB_SEARCH_URL, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json().get("results", [])
                results = []
                for item in data[:8]:
                    release_date = item.get("release_date", "")
                    year = int(release_date.split("-")[0]) if release_date else 2000
                    poster = f"{IMAGE_BASE_URL}{item.get('poster_path', '')}" if item.get("poster_path") else ""
                    results.append({
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "year": year,
                        "description": item.get("overview", "No description available."),
                        "img_url": poster or "https://via.placeholder.com/500x750?text=No+Poster"
                    })
                return results
        except Exception:
            pass

    # Filter fallback dataset
    q = query.lower()
    matches = [m for m in FALLBACK_MOVIES if q in m["title"].lower()]
    return matches if matches else FALLBACK_MOVIES[:3]


def get_movie_details(movie_id: int) -> Dict[str, Any]:
    """Gets full movie details by ID."""
    if TMDB_API_KEY != "your_tmdb_api_key_here":
        try:
            url = f"{TMDB_MOVIE_URL}/{movie_id}"
            params = {"api_key": TMDB_API_KEY}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                item = response.json()
                release_date = item.get("release_date", "")
                year = int(release_date.split("-")[0]) if release_date else 2000
                poster = f"{IMAGE_BASE_URL}{item.get('poster_path', '')}" if item.get("poster_path") else ""
                return {
                    "title": item.get("title"),
                    "year": year,
                    "description": item.get("overview", ""),
                    "img_url": poster
                }
        except Exception:
            pass

    for m in FALLBACK_MOVIES:
        if m["id"] == movie_id:
            return m

    return FALLBACK_MOVIES[0]
