import { useState } from 'react'
import { useMovieSearch } from './features/movies/queries'

import './App.css';

function App() {
  const [query, setQuery] = useState("");

    const {
    data: movies = [],
    error,
    isError,
    isFetching,
  } = useMovieSearch(query)

  return (
    <main>
      <h1>Movie recommender</h1>
      <p>Search for a movie and discover similar titles.</p>

        <input placeholder="Search for a movie" type="search" value={query} onChange={(event) => setQuery(event.target.value)} />
  

      {isError ? <p>{error.message}</p> : null}

      {
        query && !isFetching && !error && movies.length > 0 ? 
        
        <ul>
          {movies.map((movie) => {
          return <li key={movie.movie_id}>
            <strong>{movie.title}</strong>
            <div>{movie.genres.join(' | ')}</div>
          </li>
        })}
        </ul>
        
        : <p>No movies found.</p>
      }
    </main>
  )
}

export default App
