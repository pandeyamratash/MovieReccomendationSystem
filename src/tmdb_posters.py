
import json
import os
import re

import requests
from dotenv import load_dotenv

from src.config import PROCESSED_DATA_DIR


# Load environment variables from the project's .env file
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

POSTER_CACHE_PATH = PROCESSED_DATA_DIR / "tmdb_posters.json"


def load_poster_cache():
    """Load previously retrieved poster URLs from the cache."""
    if not POSTER_CACHE_PATH.exists():
        return {}

    try:
        with open(POSTER_CACHE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


def save_poster_cache(cache):
    """Save poster URLs to a JSON cache."""
    POSTER_CACHE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(POSTER_CACHE_PATH, "w", encoding="utf-8") as file:
        json.dump(cache, file, indent=2)


def get_movie_year(title):
    """Extract a four-digit year from titles such as Toy Story (1995)."""
    match = re.search(r"\((\d{4})\)\s*$", title)

    if match:
        return match.group(1)

    return None

def get_movie_poster(title):
    if not TMDB_API_KEY:
        print("TMDB_API_KEY is missing from .env")
        return None

    cache = load_poster_cache()

    # Reuse a previously retrieved poster.
    if cache.get(title):
        return cache[title]

    year = get_movie_year(title)
    search_title = re.sub(
        r"\s*\(\d{4}\)\s*$",
        "",
        title,
    ).strip()

    params = {
        "api_key": TMDB_API_KEY,
        "query": search_title,
        "include_adult": "false",
        "language": "en-US",
    }

    if year:
        params["year"] = year

    for attempt in range(2):
        try:
            response = requests.get(
                TMDB_SEARCH_URL,
                params=params,
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            poster_url = None

            # Prefer an exact title and year match.
            for movie in results:
                poster_path = movie.get("poster_path")
                if not poster_path:
                    continue

                movie_title = movie.get("title", "").strip().lower()
                movie_year = (movie.get("release_date") or "")[:4]

                if (
                    movie_title == search_title.lower()
                    and (not year or movie_year == year)
                ):
                    poster_url = f"{TMDB_IMAGE_BASE}{poster_path}"
                    break

            # Fallback to the first result with a poster.
            if poster_url is None:
                for movie in results:
                    if movie.get("poster_path"):
                        poster_url = (
                            f"{TMDB_IMAGE_BASE}{movie['poster_path']}"
                        )
                        break

            # Cache only successful API responses.
            cache[title] = poster_url
            save_poster_cache(cache)
            return poster_url

        except requests.RequestException as error:
            if attempt == 1:
                print(f"TMDB temporarily unavailable for {title}: {error}")
                return None

    return None
