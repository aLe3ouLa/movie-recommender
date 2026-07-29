from pathlib import Path

import pandas as pd


DATA_FILE = Path("data/ml-latest-small/ratings.csv")
ratings = pd.read_csv(DATA_FILE)

user_count = ratings["userId"].nunique()
movie_count = ratings["movieId"].nunique()
rating_count = len(ratings)

possible_ratings = user_count * movie_count
density = rating_count / possible_ratings
sparsity = 1 - density

print("Users:", user_count)
print("Rated movies:", movie_count)
print("Observed ratings:", rating_count)
print("Possible ratings:", possible_ratings)
print(f"Density: {density:.2%}")
print(f"Sparsity: {sparsity:.2%}")