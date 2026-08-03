import './MovieCard.css'

function initials(title) {
  return title
    .replace(/\(\d{4}\)$/, '')
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((word) => word[0])
    .join('')
    .toUpperCase()
}

export function MovieCard({ movie, matchPercent, matchLabel = 'Match', onClick }) {
  const isInteractive = typeof onClick === 'function'

  return (
    <div
      className="movie-card"
      role={isInteractive ? 'button' : undefined}
      tabIndex={isInteractive ? 0 : undefined}
      onClick={onClick}
      onKeyDown={
        isInteractive
          ? (event) => {
              if (event.key === 'Enter' || event.key === ' ') onClick(event)
            }
          : undefined
      }
    >
      <div className="movie-card__poster">
        {movie.poster_url ? (
          <img src={movie.poster_url} alt={movie.title} loading="lazy" />
        ) : (
          <span className="movie-card__placeholder">{initials(movie.title)}</span>
        )}

        {typeof matchPercent === 'number' && (
          <span className="match-badge movie-card__match">
            {Math.round(matchPercent)}% {matchLabel}
          </span>
        )}
      </div>

      <div className="movie-card__body">
        <h3 className="movie-card__title">{movie.title}</h3>
        <p className="movie-card__genres">{movie.genres.slice(0, 2).join(' · ')}</p>
        <p className="rating-badge">
          <span className="star">★</span>
          {movie.average_rating.toFixed(1)}
          <span className="movie-card__count">({movie.rating_count})</span>
        </p>
      </div>
    </div>
  )
}
