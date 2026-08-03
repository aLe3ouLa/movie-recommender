from __future__ import annotations

import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = PROJECT_ROOT / "data" / "tmdb_cache.json"

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
REQUEST_TIMEOUT = 5

try:
    _cache: dict[str, str | None] = json.loads(
        CACHE_PATH.read_text()
    )
except (FileNotFoundError, json.JSONDecodeError):
    _cache = {}


def _save_cache() -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(_cache))


def _fetch_poster_path(tmdb_id: int) -> str | None:
    cache_key = str(tmdb_id)

    if cache_key in _cache:
        return _cache[cache_key]

    poster_path = None

    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{tmdb_id}",
            params={"api_key": TMDB_API_KEY},
            timeout=REQUEST_TIMEOUT,
        )
        if response.ok:
            poster_path = response.json().get("poster_path")
    except requests.RequestException:
        poster_path = None

    _cache[cache_key] = poster_path
    _save_cache()

    return poster_path


def attach_posters(records: list[dict]) -> list[dict]:
    """Add a poster_url field to each movie dict, using its tmdb_id.

    Degrades to poster_url: None (never raises) when no API key is
    configured, a movie has no tmdb_id, or the TMDB request fails.
    """

    for record in records:
        tmdb_id = record.get("tmdb_id")

        poster_path = (
            _fetch_poster_path(tmdb_id)
            if TMDB_API_KEY and tmdb_id is not None
            else None
        )

        record["poster_url"] = (
            f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None
        )

    return records
