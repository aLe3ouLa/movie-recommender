from pathlib import Path

import pandas as pd

DATA_FILE = Path("data/ml-latest-small/movies.csv")
movies = pd.read_csv(DATA_FILE)

genre_features = movies["genres"].str.get_dummies(sep="|")

example_genres = [
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Fantasy",
]

examples = movies.iloc[:3][["title"]].join(
    genre_features.iloc[:3][example_genres]
)

print(examples.to_string(index=False))