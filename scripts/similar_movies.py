from pathlib import Path

import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = Path("data/ml-latest-small/movies.csv")

movies = pd.read_csv(DATA_FILE)
# Convert genres into 0/1 features.
genre_features = movies["genres"].str.get_dummies(sep="|")
genre_features = csr_matrix(genre_features.to_numpy())

# Remove release years before processing titles.
clean_titles = movies["title"].str.replace(
    r"\s*\(\d{4}\)$",
    "",
    regex=True,
)

# Convert title words and two-word phrases into numeric features.
title_vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
)

title_features = title_vectorizer.fit_transform(clean_titles)

# Title features receive extra weight.
movie_features = hstack([
    title_features * 2,
    genre_features,
])

def search_movies(query: str, limit: int = 10):
    matches = movies[
        movies["title"].str.contains(
            query,
            case=False,
            regex=False,
            na=False,
        )
    ]

    return matches.head(limit)

def recommend_similar_movies(title: str, number: int = 10):
    matching_movies = movies.index[movies["title"] == title]
    if matching_movies.empty:
        raise ValueError(f"Movie not fount: {title}")

    movie_index = matching_movies[0]

    similarity_scores = cosine_similarity(
        movie_features[movie_index],
        movie_features,
    )[0]

    ranked_indices = similarity_scores.argsort()[::-1]

    # Do not recommend the selected movie itself.
    ranked_indices = [
        index
        for index in ranked_indices
        if index != movie_index
    ][:number]

    recommendations = movies.iloc[ranked_indices].copy()
    recommendations["similarity"] = similarity_scores[ranked_indices]

    return recommendations


query = input("Search for a movie: ").strip()
matches = search_movies(query)

if matches.empty:
    print(f'No movies found for "{query}".')
else:
    print("\nMatching movies:")

    for option_number, title in enumerate(matches["title"], start=1):
        print(f"{option_number}. {title}")

    try:
        selection = int(input("\nChoose a number: "))

        if selection < 1 or selection > len(matches):
            raise ValueError

        selected_title = matches.iloc[selection - 1]["title"]

        print(f"\nMovies similar to {selected_title}:\n")

        results = recommend_similar_movies(selected_title)

        print(
            results[
                ["title", "genres", "similarity"]
            ].to_string(index=False)
        )

    except ValueError:
        print("Please enter one of the displayed numbers.")