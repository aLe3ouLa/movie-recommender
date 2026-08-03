import { useState } from 'react'
import { useGenres, useMoviesByGenre } from './queries'
import { MovieCard } from './MovieCard'
import './GenrePicker.css'

const FEATURED_GENRES = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Thriller', 'Romance']

export function GenrePicker({ onSelectMovie }) {
  const [activeGenre, setActiveGenre] = useState('Action')
  const { data: allGenres = [] } = useGenres()
  const { data: movies = [], isLoading, isError } = useMoviesByGenre(activeGenre, 10)

  const tabs = allGenres.length
    ? FEATURED_GENRES.filter((genre) => allGenres.includes(genre))
    : FEATURED_GENRES

  return (
    <section id="genres">
      <div className="container">
        <div className="section-heading">
          <span className="eyebrow">Browse by Genre</span>
          <h2>Top Picks in Every Genre</h2>
          <p>The best-rated movies within each genre, ranked the same way as the popular list.</p>
        </div>

        <div className="pill-tabs genre-picker__tabs">
          {tabs.map((genre) => (
            <button
              key={genre}
              className={`pill-tab ${genre === activeGenre ? 'is-active' : ''}`}
              onClick={() => setActiveGenre(genre)}
            >
              {genre}
            </button>
          ))}
        </div>

        {isLoading && <p className="state-message">Loading {activeGenre.toLowerCase()} picks…</p>}
        {isError && <p className="state-message">Couldn't load this genre.</p>}

        {!isLoading && !isError && (
          <div className="movie-grid">
            {movies.map((movie) => (
              <MovieCard
                key={movie.movie_id}
                movie={movie}
                onClick={() => onSelectMovie(movie)}
              />
            ))}
          </div>
        )}
      </div>
    </section>
  )
}
