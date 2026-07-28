from pathlib import Path
import pandas as pd

DATA_FILE = Path("data/ml-latest-small/movies.csv")
movies = pd.read_csv(DATA_FILE)

RATINGS_FILE = Path("data/ml-latest-small/ratings.csv")
ratings = pd.read_csv(RATINGS_FILE)

print("Number of movies: ", len(movies))
print("\nColumns: ", movies.columns.tolist())
print("\nFirst fice movies:")

print(movies.head(10));

print("\nMissing values:")
print(movies.isna().sum())

print("\nDuplicate movie IDs:")
print(movies["movieId"].duplicated().sum())

print("\nComedy movies:")
comedy_movies = movies[movies["genres"].str.contains("Comedy")]
print(comedy_movies[["title", "genres"]].head(10))
print("Total:", len(comedy_movies))

genre_counts = (
    movies["genres"]
    .str.split("|")
    .explode()
    .value_counts()
)

print(genre_counts)

print("\nRatings shape:", ratings.shape)
print("\nRatings columns:", ratings.columns.tolist())
print("\nFirst five ratings:")
print(ratings.head())

print("\nRating distribution:")
print(ratings["rating"].value_counts().sort_index())