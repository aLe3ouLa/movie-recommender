from pathlib import Path

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer


DATA_DIR = Path("data/ml-latest-small")

movies = pd.read_csv(DATA_DIR / "movies.csv")
ratings = pd.read_csv(DATA_DIR / "ratings.csv")

# A rating of 4 or more represents a liked movie.
liked_ratings = ratings[
    ratings["rating"] >= 4
].sort_values(
    by=["userId", "timestamp"]
)

# Evaluation requires at least one seed movie and one target movie.
likes_per_user = liked_ratings.groupby("userId").size()

eligible_users = likes_per_user[
    likes_per_user >= 2
].index

eligible_likes = liked_ratings[
    liked_ratings["userId"].isin(eligible_users)
]

# Hide each user's most recently liked movie.
test_ratings = (
    eligible_likes
    .groupby("userId")
    .tail(1)
    .copy()
)

# Everything else remains available for model building.
train_ratings = ratings.drop(
    index=test_ratings.index
)

# Use the user's previous liked movie as the recommendation seed.
remaining_likes = eligible_likes.drop(
    index=test_ratings.index
)

seed_ratings = (
    remaining_likes
    .groupby("userId")
    .tail(1)
    [["userId", "movieId"]]
    .rename(columns={"movieId": "seed_movie_id"})
)

evaluation_cases = seed_ratings.merge(
    test_ratings[["userId", "movieId"]],
    on="userId",
)

evaluation_cases = evaluation_cases.rename(
    columns={"movieId": "target_movie_id"}
)

movie_titles = movies.set_index("movieId")["title"]

print("Original ratings:", len(ratings))
print("Training ratings:", len(train_ratings))
print("Hidden test ratings:", len(test_ratings))
print("Evaluation users:", len(evaluation_cases))

print("\nExample evaluation cases:")

for case in evaluation_cases.head(5).itertuples():
    print(f"\nUser {case.userId}")
    print("Seed:", movie_titles[case.seed_movie_id])
    print("Hidden target:", movie_titles[case.target_movie_id])
# Give every movie and user a matrix position.
movie_ids = pd.Index(movies["movieId"])
user_ids = pd.Index(sorted(train_ratings["userId"].unique()))

movie_positions = {
    movie_id: position
    for position, movie_id in enumerate(movie_ids)
}

user_positions = {
    user_id: position
    for position, user_id in enumerate(user_ids)
}

rows = train_ratings["movieId"].map(movie_positions)
columns = train_ratings["userId"].map(user_positions)

# Build the matrix using training data only.
training_matrix = csr_matrix(
    (
        train_ratings["rating"],
        (rows, columns),
    ),
    shape=(len(movie_ids), len(user_ids)),
)

hits = 0
recommendation_limit = 10

for case in evaluation_cases.itertuples():
    seed_position = movie_positions[case.seed_movie_id]
    target_position = movie_positions[case.target_movie_id]

    similarity_scores = cosine_similarity(
        training_matrix[seed_position],
        training_matrix,
    )[0]

    # Do not recommend the seed movie itself.
    similarity_scores[seed_position] = -1

    recommended_positions = (
        similarity_scores
        .argsort()[::-1][:recommendation_limit]
    )

    if target_position in recommended_positions:
        hits += 1

hit_rate = hits / len(evaluation_cases)

print(f"\nHits: {hits}")
print(f"Evaluation cases: {len(evaluation_cases)}")
print(f"Hit Rate@{recommendation_limit}: {hit_rate:.2%}")

movie_popularity = (
    train_ratings
    .groupby("movieId")
    .size()
    .sort_values(ascending=False)
)

popular_movie_ids = movie_popularity.index.tolist()

popularity_hits = 0

for case in evaluation_cases.itertuples():
    # Use the most popular movies, excluding the seed.
    recommendations = [
        movie_id
        for movie_id in popular_movie_ids
        if movie_id != case.seed_movie_id
    ][:recommendation_limit]

    if case.target_movie_id in recommendations:
        popularity_hits += 1

popularity_hit_rate = (
    popularity_hits / len(evaluation_cases)
)

print("\nPopularity baseline")
print("Hits:", popularity_hits)
print(
    f"Hit Rate@{recommendation_limit}: "
    f"{popularity_hit_rate:.2%}"
)

# Build content features.
genre_features = csr_matrix(
    movies["genres"]
    .str.get_dummies(sep="|")
    .to_numpy()
)

clean_titles = movies["title"].str.replace(
    r"\s*\(\d{4}\)$",
    "",
    regex=True,
)

title_features = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
).fit_transform(clean_titles)

content_features = hstack([
    title_features * 2,
    genre_features,
])

# Calculate rating quality using training data only.
global_average = train_ratings["rating"].mean()
rating_prior = 25

training_stats = (
    train_ratings
    .groupby("movieId")["rating"]
    .agg(["mean", "count"])
)

average_ratings = (
    training_stats["mean"]
    .reindex(movie_ids)
    .fillna(global_average)
    .to_numpy()
)

rating_counts = (
    training_stats["count"]
    .reindex(movie_ids)
    .fillna(0)
    .to_numpy()
)

weighted_ratings = (
    rating_counts / (rating_counts + rating_prior)
    * average_ratings
    + rating_prior / (rating_counts + rating_prior)
    * global_average
)

normalized_ratings = weighted_ratings / 5

content_hits = 0
hybrid_hits = 0

for case in evaluation_cases.itertuples():
    seed_position = movie_positions[case.seed_movie_id]
    target_position = movie_positions[case.target_movie_id]

    content_scores = cosine_similarity(
        content_features[seed_position],
        content_features,
    )[0]

    collaborative_scores = cosine_similarity(
        training_matrix[seed_position],
        training_matrix,
    )[0]

    hybrid_scores = (
        content_scores * 0.55
        + collaborative_scores * 0.30
        + normalized_ratings * 0.15
    )

    content_scores[seed_position] = -1
    hybrid_scores[seed_position] = -1

    unrelated = (
        (content_scores == 0)
        & (collaborative_scores == 0)
    )

    hybrid_scores[unrelated] = -1

    content_recommendations = (
        content_scores.argsort()[::-1][:recommendation_limit]
    )

    hybrid_recommendations = (
        hybrid_scores.argsort()[::-1][:recommendation_limit]
    )

    if target_position in content_recommendations:
        content_hits += 1

    if target_position in hybrid_recommendations:
        hybrid_hits += 1

content_hit_rate = content_hits / len(evaluation_cases)
hybrid_hit_rate = hybrid_hits / len(evaluation_cases)

print("\nContent model")
print("Hits:", content_hits)
print(f"Hit Rate@10: {content_hit_rate:.2%}")

print("\nHybrid model")
print("Hits:", hybrid_hits)
print(f"Hit Rate@10: {hybrid_hit_rate:.2%}")