from pathlib import Path

import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np


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

# Convert movie × user into user × movie.
user_movie_features = collaborative_features.T.tocsr()

user_average_ratings = (
    ratings.groupby("userId")["rating"]
    .mean()
    .reindex(user_ids)
    .to_numpy()
)

# Center each observed rating around that user's average.
centered_user_features = (
    user_movie_features
    .copy()
    .astype(float)
)

ratings_per_user = np.diff(
    centered_user_features.indptr
)

centered_user_features.data -= np.repeat(
    user_average_ratings,
    ratings_per_user,
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

def get_movie_index(movie_id: int) -> int:
    matching_movies = movies.index[
        movies["movieId"] == movie_id
    ]

    if matching_movies.empty:
        raise ValueError(f"Movie not found: {movie_id}")

    return int(matching_movies[0])


def movie_record(index: int) -> dict:
    movie = movies.iloc[index]

    return {
        "movie_id": int(movie["movieId"]),
        "title": movie["title"],
        "genres": movie["genres"].split("|"),
        "average_rating": round(
            float(movie["average_rating"]),
            2,
        ),
        "rating_count": int(movie["rating_count"]),
    }


def top_indices(
    scores,
    selected_index: int,
    limit: int,
):
    scores = scores.copy()
    scores[selected_index] = -1

    ranked = scores.argsort()[::-1]

    return [
        index
        for index in ranked
        if scores[index] > 0
    ][:limit]

def find_similar_movies(
    movie_id: int,
    limit: int = 10,
) -> list[dict]:
    """Find movies with similar titles and genres."""

    movie_index = get_movie_index(movie_id)

    content_scores = cosine_similarity(
        movie_features[movie_index],
        movie_features,
    )[0]

    ranked_indices = top_indices(
        content_scores,
        selected_index=movie_index,
        limit=limit,
    )

    return [
        {
            **movie_record(index),
            "content_similarity": round(
                float(content_scores[index]),
                3,
            ),
        }
        for index in ranked_indices
    ]

def find_audience_also_liked(
    movie_id: int,
    limit: int = 10,
) -> list[dict]:
    """Find movies with similar audience-rating patterns."""

    movie_index = get_movie_index(movie_id)

    collaborative_scores = cosine_similarity(
        collaborative_features[movie_index],
        collaborative_features,
    )[0]

    ranked_indices = top_indices(
        collaborative_scores,
        selected_index=movie_index,
        limit=limit,
    )

    return [
        {
            **movie_record(index),
            "collaborative_similarity": round(
                float(collaborative_scores[index]),
                3,
            ),
        }
        for index in ranked_indices
    ]

def recommend_for_user(
    user_id: int,
    limit: int = 10,
    neighbor_limit: int = 30,
) -> list[dict]:
    """Recommend unseen movies using similar users."""

    if user_id not in user_positions:
        raise ValueError(f"User not found: {user_id}")

    user_index = user_positions[user_id]

    user_similarities = cosine_similarity(
        centered_user_features[user_index],
        centered_user_features,
    )[0]

    # A user should not be their own neighbor.
    user_similarities[user_index] = -1

    neighbor_indices = (
        user_similarities
        .argsort()[::-1]
    )

    neighbor_indices = [
        index
        for index in neighbor_indices
        if user_similarities[index] > 0
    ][:neighbor_limit]

    if not neighbor_indices:
        return []

    neighbor_similarities = user_similarities[
        neighbor_indices
    ]

    neighbor_preferences = centered_user_features[
        neighbor_indices
    ]

    # Track which neighbors rated each movie.
    neighbor_rating_mask = neighbor_preferences.copy()
    neighbor_rating_mask.data = np.ones_like(
        neighbor_rating_mask.data
    )

    weighted_preferences = np.asarray(
        neighbor_preferences.T.dot(
            neighbor_similarities
        )
    ).ravel()

    similarity_totals = np.asarray(
        neighbor_rating_mask.T.dot(
            neighbor_similarities
        )
    ).ravel()

    support_counts = np.asarray(
        neighbor_rating_mask.sum(axis=0)
    ).ravel()

    minimum_support = 3
    confidence_prior = 20

    supported_movies = (
        (similarity_totals > 0)
        & (support_counts >= minimum_support)
    )

    predicted_ratings = np.full(
        len(movies),
        -np.inf,
    )

    preference_adjustments = np.zeros(
        len(movies)
    )

    preference_adjustments[supported_movies] = (
        weighted_preferences[supported_movies]
        / similarity_totals[supported_movies]
    )

    confidence = (
        support_counts
        / (support_counts + confidence_prior)
    )

    predicted_ratings[supported_movies] = (
        user_average_ratings[user_index]
        + preference_adjustments[supported_movies]
        * confidence[supported_movies]
    )

    predicted_ratings = np.clip(
        predicted_ratings,
        0.5,
        5,
    )

    # Never recommend movies this user already rated.
    seen_movie_indices = (
        user_movie_features[user_index].indices
    )

    predicted_ratings[seen_movie_indices] = -np.inf

    ranked_indices = predicted_ratings.argsort()[::-1]

    ranked_indices = [
        index
        for index in ranked_indices
        if np.isfinite(predicted_ratings[index])
    ][:limit]

    return [
        {
            **movie_record(index),
            "predicted_rating": round(
                float(predicted_ratings[index]),
                2,
            ),
            "supporting_neighbors": int(
                support_counts[index]
            ),
        }
        for index in ranked_indices
    ]
