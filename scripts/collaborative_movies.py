from pathlib import Path

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity


DATA_DIR = Path("data/ml-latest-small")

movies = pd.read_csv(DATA_DIR / "movies.csv")
ratings = pd.read_csv(DATA_DIR / "ratings.csv")

# Assign every movie and user a numeric matrix position.
movie_ids = pd.Index(sorted(ratings["movieId"].unique()))
user_ids = pd.Index(sorted(ratings["userId"].unique()))

movie_positions = {
    movie_id: position
    for position, movie_id in enumerate(movie_ids)
}

user_positions = {
    user_id: position
    for position, user_id in enumerate(user_ids)
}

rows = ratings["movieId"].map(movie_positions)
columns = ratings["userId"].map(user_positions)

rating_matrix = csr_matrix(
    (
        ratings["rating"],
        (rows, columns),
    ),
    shape=(len(movie_ids), len(user_ids)),
)


def recommend_from_ratings(movie_id: int, limit: int = 10):
    if movie_id not in movie_positions:
        raise ValueError(f"Movie has no ratings: {movie_id}")

    movie_position = movie_positions[movie_id]

    similarity_scores = cosine_similarity(
        rating_matrix[movie_position],
        rating_matrix,
    )[0]

    similarity_scores[movie_position] = -1

    ranked_positions = similarity_scores.argsort()[::-1][:limit]

    recommendations = []

    for position in ranked_positions:
        recommended_id = movie_ids[position]

        movie = movies[
            movies["movieId"] == recommended_id
        ].iloc[0]

        recommendations.append({
            "title": movie["title"],
            "similarity": round(
                float(similarity_scores[position]),
                3,
            ),
        })

    return recommendations


for recommendation in recommend_from_ratings(1):
    print(recommendation)