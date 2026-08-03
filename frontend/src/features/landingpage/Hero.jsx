import { usePopularMovies } from '../movies/queries'
import './hero.css'

export function Hero() {
  const { data: popular = [] } = usePopularMovies(3)
  const spotlight = popular[0]

  return (
    <section id="top" className="hero">
      <div className="container hero__inner">
        <div className="hero__copy">
          <span className="eyebrow">A machine learning systems project</span>
          <h1>Find your next favorite movie</h1>
          <p>
            Personalized recommendations built on content-based filtering, item- and
            user-based collaborative filtering, and a hybrid ranking model — trained on
            the MovieLens dataset.
          </p>
          <div className="hero__actions">
            <a className="btn btn-primary" href="#recommendations">
              Browse Recommendations
            </a>
            <a className="btn btn-secondary" href="#about">
              How It Works
            </a>
          </div>
        </div>

        <div className="hero__visual">
          <div className="hero__posters">
            {popular.slice(0, 3).map((movie, index) => (
              <div key={movie.movie_id} className={`hero__poster hero__poster--${index}`}>
                {movie.poster_url ? (
                  <img src={movie.poster_url} alt={movie.title} />
                ) : (
                  <span>{movie.title}</span>
                )}
              </div>
            ))}
          </div>

          {spotlight && (
            <div className="hero__match-card">
              <div className="hero__match-thumb">
                {spotlight.poster_url ? (
                  <img src={spotlight.poster_url} alt={spotlight.title} />
                ) : (
                  <span>🎬</span>
                )}
              </div>
              <div>
                <span className="match-badge">
                  {Math.round((spotlight.average_rating / 5) * 100)}% Match
                </span>
                <p className="hero__match-title">{spotlight.title}</p>
                <p className="rating-badge">
                  <span className="star">★</span>
                  {spotlight.average_rating.toFixed(1)} ({spotlight.rating_count} ratings)
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}
