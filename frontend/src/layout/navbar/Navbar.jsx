import { useState } from 'react'
import { useMovieSearch } from '../../features/movies/queries'
import { useDebouncedValue } from '../../features/movies/useDebouncedValue'
import './navbar.css'

export function Navbar({ onSelectMovie, viewerId, onViewerIdChange }) {
  const [query, setQuery] = useState('')
  const [isFocused, setIsFocused] = useState(false)
  const debouncedQuery = useDebouncedValue(query, 300)

  const { data: results = [], isFetching } = useMovieSearch(debouncedQuery)

  const showDropdown = isFocused && debouncedQuery.trim().length >= 2

  function handleSelect(movie) {
    onSelectMovie(movie)
    setQuery('')
    setIsFocused(false)
  }

  return (
    <header className="navbar">
      <div className="container navbar__inner">
        <a className="navbar__brand" href="#top">
          <span className="navbar__logo" aria-hidden="true">
            🍿
          </span>
          Popcorn Picks
        </a>

        <div className="navbar__search">
          <input
            type="search"
            placeholder="Search movies, e.g. Toy Story…"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setTimeout(() => setIsFocused(false), 120)}
          />

          {showDropdown && (
            <div className="navbar__results">
              {isFetching && <p className="navbar__results-empty">Searching…</p>}

              {!isFetching && results.length === 0 && (
                <p className="navbar__results-empty">No movies found.</p>
              )}

              {!isFetching &&
                results.slice(0, 8).map((movie) => (
                  <button
                    key={movie.movie_id}
                    className="navbar__result"
                    onMouseDown={() => handleSelect(movie)}
                  >
                    <strong>{movie.title}</strong>
                    <span>{movie.genres.slice(0, 3).join(' · ')}</span>
                  </button>
                ))}
            </div>
          )}
        </div>

        <nav className="navbar__links">
          <a href="#recommendations">Home</a>
          <a href="#about">How It Works</a>
        </nav>

        <div className="navbar__viewer">
          <label htmlFor="viewer-id">Viewing as</label>
          <input
            id="viewer-id"
            type="number"
            min="1"
            max="610"
            placeholder="User ID"
            value={viewerId}
            onChange={(event) => onViewerIdChange(event.target.value)}
          />
        </div>
      </div>
    </header>
  )
}
