import { useUserRecommendations } from './queries'
import './PredictedScore.css'

export function PredictedScore({ viewerId, onViewerIdChange }) {
  const {
    data: movies = [],
    isFetching,
    isError,
    error,
  } = useUserRecommendations(viewerId, 6)

  return (
    <section id="predicted-score" className="predicted-score">
      <div className="container predicted-score__inner">
        <div className="predicted-score__copy">
          <span className="eyebrow">Personalized, Not Guessed</span>
          <h2>See how much you'll enjoy a movie</h2>
          <p>
            This runs a real user-based collaborative filtering model: it finds the
            MovieLens viewers whose ratings best match a given user, then predicts a
            rating for everything that user hasn't seen yet.
          </p>

          <label className="predicted-score__input-label" htmlFor="predicted-score-user">
            Try it — enter any MovieLens user ID (1–610)
          </label>
          <input
            id="predicted-score-user"
            type="number"
            min="1"
            max="610"
            placeholder="e.g. 42"
            value={viewerId}
            onChange={(event) => onViewerIdChange(event.target.value)}
          />
        </div>

        <div className="predicted-score__list">
          {!viewerId && (
            <p className="state-message">Enter a user ID to generate predictions.</p>
          )}

          {viewerId && isFetching && <p className="state-message">Predicting…</p>}

          {viewerId && isError && <p className="state-message">{error.message}</p>}

          {viewerId && !isFetching && !isError && movies.length === 0 && (
            <p className="state-message">
              Not enough similar viewers to make a confident prediction for this user.
            </p>
          )}

          {viewerId &&
            !isFetching &&
            !isError &&
            movies.map((movie) => {
              const percent = Math.round((movie.predicted_rating / 5) * 100)

              return (
                <div key={movie.movie_id} className="predicted-row">
                  <div className="predicted-row__thumb">
                    {movie.poster_url ? (
                      <img src={movie.poster_url} alt={movie.title} />
                    ) : (
                      <span>🎬</span>
                    )}
                  </div>

                  <div className="predicted-row__body">
                    <p className="predicted-row__title">{movie.title}</p>
                    <div className="predicted-row__bar">
                      <div className="predicted-row__bar-fill" style={{ width: `${percent}%` }} />
                    </div>
                    <p className="predicted-row__meta">
                      Predicted {movie.predicted_rating.toFixed(1)} / 5 · based on{' '}
                      {movie.supporting_neighbors} similar viewers
                    </p>
                  </div>

                  <span className="predicted-row__percent">{percent}%</span>
                </div>
              )
            })}
        </div>
      </div>
    </section>
  )
}
