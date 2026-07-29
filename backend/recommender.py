from pathlib import Path

import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data/ml-latest-small"

movies = pd.read_csv(DATA_DIR / "movies.csv")
ratings = pd.read_csv(DATA_DIR / "ratings.csv")

GLOBAL_AVERAGE = ratings["rating"].mean()
RATING_PRIOR = 25

rating_stats = (
    ratings.groupby("movieId")
    .agg(
        average_rating=("rating", "mean"),
        rating_count=("rating", "count"),
    )
    .reset_index()
)

movies = movies.merge(
    rating_stats,
    on="movieId",
    how="left",
)

movies["rating_count"] = (
    movies["rating_count"]
    .fillna(0)
    .astype(int)
)

movies["average_rating"] = (
    movies["average_rating"]
    .fillna(GLOBAL_AVERAGE)
)

rating_count = movies["rating_count"]
average_rating = movies["average_rating"]

movies["weighted_rating"] = (
    rating_count / (rating_count + RATING_PRIOR)
    * average_rating
    + RATING_PRIOR / (rating_count + RATING_PRIOR)
    * GLOBAL_AVERAGE
)

movie_positions = {
    movie_id: position
    for position, movie_id in enumerate(movies["movieId"])
}

user_ids = pd.Index(sorted(ratings["userId"].unique()))

user_positions = {
    user_id: position
    for position, user_id in enumerate(user_ids)
}

rating_rows = ratings["movieId"].map(movie_positions)
rating_columns = ratings["userId"].map(user_positions)

collaborative_features = csr_matrix(
    (
        ratings["rating"],
        (rating_rows, rating_columns),
    ),
    shape=(len(movies), len(user_ids)),
)

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

    content_scores = cosine_similarity(
        movie_features[movie_index],
        movie_features,
    )[0]

    collaborative_scores = cosine_similarity(
        collaborative_features[movie_index],
        collaborative_features,
    )[0]

    normalized_ratings = (
        movies["weighted_rating"].to_numpy() / 5
    )

    ranking_scores = (
        content_scores * 0.55
        + collaborative_scores * 0.30
        + normalized_ratings * 0.15
    )

    # Exclude the selected movie itself.
    ranking_scores[movie_index] = -1

    # Require at least some content or behavioral relationship.
    unrelated_movies = (
        (content_scores == 0)
        & (collaborative_scores == 0)
    )

    # Exclude the selected movie.
    ranking_scores[unrelated_movies] = -1

    ranked_indices = ranking_scores.argsort()[::-1][:limit]

    return [
        {
            "movie_id": int(movies.iloc[index]["movieId"]),
            "title": movies.iloc[index]["title"],
            "genres": movies.iloc[index]["genres"].split("|"),
            "similarity": round(
                float(content_scores[index]),
                3,
            ),
            "collaborative_similarity": round(
                float(collaborative_scores[index]),
                3,
            ),
            "average_rating": round(
                float(movies.iloc[index]["average_rating"]),
                2,
            ),
            "rating_count": int(
                movies.iloc[index]["rating_count"],
            ),
            "ranking_score": round(
                float(ranking_scores[index]),
                3,
            ),
        }
        for index in ranked_indices
    ]