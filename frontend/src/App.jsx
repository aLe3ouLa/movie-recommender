import { useState } from 'react'
import { useMovieSearch, useMovieRecommendations } from './features/movies/queries'
import { useDebouncedValue } from './features/movies/useDebouncedValue'
import './App.css';

function App() {
  const [query, setQuery] = useState("");
  const [selectedMovieId, setSelectedMovieId] = useState("");

  const debouncedQuery = useDebouncedValue(query, 300)

  const {
    data: movies = [],
    error,
    isError,
    isFetching,
  } = useMovieSearch(debouncedQuery)

  const {
    data: recommendations = [],
    error: recommendationError,
    isError: isRecommendationError,
    isFetching: isLoadingRecommendations,
  } = useMovieRecommendations(selectedMovieId)

  function handleQueryChange(event) {
    setQuery(event.target.value)
    setSelectedMovieId(null)
  }

  return (
    <main>
      <h1>Movie recommender</h1>
      <p>Search for a movie and discover similar titles.</p>

      <input placeholder="Search for a movie" type="search" value={query} onChange={handleQueryChange} />

      {selectedMovieId}
      {isError ? <p>{error.message}</p> : null}

      {

        query && !isFetching && !error && movies.length > 0 ?

          <div>
            {movies.map((movie) => {
              return <button key={movie.movie_id} onClick={() => setSelectedMovieId(movie.movie_id)}>
                <strong>{movie.title}</strong>
                <div>{movie.genres.join(' | ')}</div>
              </button>
            })}
          </div>

          : <p>No movies found.</p>
      }

      {selectedMovieId && <section>
        <h2>Movies similar to {movies.filter(movie => movie.movieId === selectedMovieId)?.[0]?.title}</h2>

        {isLoadingRecommendations && (
          <p>Finding recommendations…</p>
        )}

        {isRecommendationError && (
          <p>{recommendationError.message}</p>
        )}

        {!isLoadingRecommendations && (
          <ul>
            {recommendations.map((movie) => (
              <li key={movie.movie_id}>
                <strong>{movie.title}</strong>
                <div>{movie.genres.join(' · ')}</div>
                <div>
                  Similarity: {Math.round(movie.similarity * 100)}%
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>}
    </main>
  )
}

export default App
