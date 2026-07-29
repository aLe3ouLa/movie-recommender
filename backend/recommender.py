from pathlib import Path

import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data/ml-latest-small/movies.csv"

movies = pd.read_csv(DATA_FILE)

genre_features = movies["genres"].str.get_dummies(sep="|")
genre_features = csr_matrix(genre_features.to_numpy())

clean_titles = movies["title"].str.replace(
    r"\s*\(\d{4}\)$",
    "",
    regex=True,
)

title_vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
)

title_features = title_vectorizer.fit_transform(clean_titles)

movie_features = hstack([
    title_features * 2,
    genre_features,
])


def search_movies(query: str, limit: int = 10) -> list[dict]:
    """Find movies whose titles contain the query."""

    matches = movies[
        movies["title"].str.contains(
            query,
            case=False,
            regex=False,
            na=False,
        )
    ].head(limit)

    return [
        {
            "movie_id": int(row.movieId),
            "title": row.title,
            "genres": row.genres.split("|"),
        }
        for row in matches.itertuples()
    ]


def recommend_similar_movies(
    movie_id: int,
    limit: int = 10,
) -> list[dict]:
    """Return movies most similar to the selected movie."""

    matching_movies = movies.index[movies["movieId"] == movie_id]

    if matching_movies.empty:
        raise ValueError(f"Movie not found: {movie_id}")

    movie_index = matching_movies[0]

    similarity_scores = cosine_similarity(
        movie_features[movie_index],
        movie_features,
    )[0]

    ranked_indices = similarity_scores.argsort()[::-1]

    ranked_indices = [
        index
        for index in ranked_indices
        if index != movie_index
    ][:limit]

    return [
        {
            "movie_id": int(movies.iloc[index]["movieId"]),
            "title": movies.iloc[index]["title"],
            "genres": movies.iloc[index]["genres"].split("|"),
            "similarity": round(float(similarity_scores[index]), 3),
        }
        for index in ranked_indices
    ]