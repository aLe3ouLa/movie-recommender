# Popcorn Picks

A study project for learning how recommender systems are built end-to-end: a FastAPI
backend that implements content-based, collaborative, and hybrid filtering over the
[MovieLens](https://grouplens.org/datasets/movielens/) `ml-latest-small` dataset, and a
React frontend that puts every model in front of a real UI.

## Architecture

- **`backend/recommender.py`** — loads `movies.csv`/`ratings.csv`/`links.csv` into pandas
  at startup and builds, in memory:
  - **Content-based features**: TF-IDF (1–2 grams) over cleaned titles + one-hot genres,
    compared with cosine similarity.
  - **Item-based collaborative features**: a sparse movie × user rating matrix, compared
    with cosine similarity ("audience also liked").
  - **User-based collaborative features**: the same matrix transposed and mean-centered
    per user, used to find similar viewers and predict ratings for unseen movies.
  - A **hybrid ranking** that blends content similarity (55%), collaborative similarity
    (30%), and a Bayesian-weighted average rating (15%).
- **`backend/tmdb.py`** — an optional, disk-cached client that resolves poster images
  from [TMDB](https://www.themoviedb.org/) using the `tmdbId` column in `links.csv`. The
  app runs fine without it (movie cards fall back to a placeholder).
- **`backend/main.py`** — a FastAPI app exposing search, popular/genre browsing, and all
  three recommendation strategies.
- **`frontend/`** — a Vite + React app (no router; one scrolling page) that composes the
  hero, popular/genre browsing, a three-tab recommendations panel (hybrid / content /
  collaborative), and a personalized "predicted score" section driven by the user-based
  model.

## Setup

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# optional: enables real posters
cp .env.example .env
# then put a free TMDB API key (https://www.themoviedb.org/settings/api) in .env

uvicorn backend.main:app --reload
```

The dataset lives in `data/ml-latest-small/` — see `data/ml-latest-small/README.txt` for
its own license terms (non-commercial use, attribution required).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server expects the API at `http://127.0.0.1:8000` by default; override with a
`VITE_API_URL` env var if needed.

## Recommendation endpoints

| Endpoint | Model |
|---|---|
| `GET /movies/search?query=` | Substring title search |
| `GET /movies/popular` | Bayesian-weighted average rating |
| `GET /movies/genres` | Distinct genre list |
| `GET /movies/genre/{genre}` | Top-rated movies within a genre |
| `GET /movies/{id}/recommendations` | Hybrid (content + collaborative + rating) |
| `GET /movies/{id}/similar` | Pure content-based |
| `GET /movies/{id}/audience-also-liked` | Pure item-based collaborative |
| `GET /users/{id}/recommendations` | User-based collaborative (`id` is any MovieLens user, 1–610) |

## Attribution

- Ratings and movie metadata: MovieLens `ml-latest-small`, GroupLens Research,
  non-commercial use only.
- Poster images: this product uses the TMDB API but is not endorsed or certified by
  TMDB.
