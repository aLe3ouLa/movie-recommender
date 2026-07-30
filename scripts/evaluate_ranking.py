from backend.recommender import recommend_similar_movies


EVALUATION_CASES = [
    {
        "name": "Toy Story franchise",
        "selected_movie_id": 1,
        "relevant_movie_ids": {
            3114,   # Toy Story 2
            78499,  # Toy Story 3
        },
    },
    {
        "name": "Star Wars original and prequel films",
        "selected_movie_id": 260,
        "relevant_movie_ids": {
            1196,   # Empire Strikes Back
            1210,   # Return of the Jedi
            2628,   # Phantom Menace
            33493,  # Revenge of the Sith
            5378,   # Attack of the Clones
        },
    },
]


recall_scores = []

for case in EVALUATION_CASES:
    recommendations = recommend_similar_movies(
        case["selected_movie_id"],
        limit=5,
    )

    recommended_ids = {
        movie["movie_id"]
        for movie in recommendations
    }

    relevant_ids = case["relevant_movie_ids"]
    matches = recommended_ids & relevant_ids

    recall = len(matches) / len(relevant_ids)
    recall_scores.append(recall)

    print(f"\n{case['name']}")
    print("Relevant recommendations found:", len(matches))
    print("Total relevant movies:", len(relevant_ids))
    print(f"Recall@5: {recall:.0%}")

mean_recall = sum(recall_scores) / len(recall_scores)

print(f"\nMean Recall@5: {mean_recall:.0%}")