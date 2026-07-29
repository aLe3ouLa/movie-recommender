from fastapi import FastAPI, Query

from backend.recommender import search_movies

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