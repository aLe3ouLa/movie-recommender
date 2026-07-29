from fastapi import FastAPI, HTTPException, Query

from backend.recommender import ( recommend_similar_movies, search_movies)

app = FastAPI(
    title="Movie Recommender API",
    version="0.1.0",
)

@app.get("/")
def home():
    return {"message": "Movie Recommender API is running"}


@app.get("/movies/search")
def search(
    query: str = Query(min_length=1, max_length=100),
):
    return search_movies(query)

@app.get("/movies/{movie_id}/recommendations")
def recommendations(
    movie_id: int,
    limit: int = Query(default=10, ge=1, le=50)
): 
    try:
        return recommend_similar_movies(
            movie_id=movie_id,
            limit=limit
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error