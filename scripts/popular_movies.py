from pathlib import Path
import pandas as pd

DATA_DIR = Path('data/ml-latest-small')

movies = pd.read_csv(DATA_DIR / "movies.csv")
ratings = pd.read_csv(DATA_DIR / "ratings.csv")

movie_stats = (
    ratings.groupby("movieId")
    .agg(
        average_rating=("rating", "mean"),
        rating_count=("rating", "count")
    )
    .reset_index()
)

popular_movies = movie_stats[movie_stats["rating_count"] >= 100]

recommendations = (
    popular_movies
    .merge(movies, on="movieId")
    .sort_values(
        by=["average_rating", "rating_count"],
        ascending=False
    )
)

print(
    recommendations[
        ["title", "genres", "average_rating", "rating_count"]
    ].head(10).to_string(index = False)
)