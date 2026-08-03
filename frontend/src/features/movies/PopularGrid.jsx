import { usePopularMovies } from './queries'
import { MovieCard } from './MovieCard'

export function PopularGrid({ onSelectMovie }) {
  const { data: movies = [], isLoading, isError } = usePopularMovies(12)

  return (
    <section id="recommendations">
      <div className="container">
        <div className="section-heading">
          <span className="eyebrow">Top Rated</span>
          <h2>Popular Right Now</h2>
          <p>
            The highest-rated titles in the catalog, ranked with a Bayesian-weighted
            average so a handful of 5-star ratings can't outrank a movie thousands of
            people have watched. Pick one to see how each recommendation model responds.
          </p>
        </div>

        {isLoading && <p className="state-message">Loading popular movies…</p>}
        {isError && <p className="state-message">Couldn't load popular movies.</p>}

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
