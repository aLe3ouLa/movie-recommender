import { useState } from 'react'
import {
  useMovieRecommendations,
  useSimilarMovies,
  useAudienceAlsoLiked,
} from './queries'
import { MovieCard } from './MovieCard'
import './RecommendationsPanel.css'

const TABS = [
  {
    key: 'hybrid',
    label: 'Hybrid Picks',
    description:
      'Blends content similarity, audience behavior, and overall rating into a single ranking.',
    scoreField: 'ranking_score',
    matchLabel: 'Match',
  },
  {
    key: 'content',
    label: 'Similar Content',
    description: 'Movies with the closest title and genre profile, via TF-IDF cosine similarity.',
    scoreField: 'content_similarity',
    matchLabel: 'Similar',
  },
  {
    key: 'collaborative',
    label: 'Audience Also Liked',
    description:
      "Movies rated similarly by the same viewers — item-based collaborative filtering.",
    scoreField: 'collaborative_similarity',
    matchLabel: 'Fans Liked',
  },
]

export function RecommendationsPanel({ movieId, movieTitle, onSelectMovie }) {
  const [activeTabKey, setActiveTabKey] = useState('hybrid')

  const hybrid = useMovieRecommendations(movieId)
  const content = useSimilarMovies(movieId)
  const collaborative = useAudienceAlsoLiked(movieId)

  const queriesByTab = { hybrid, content, collaborative }
  const activeTab = TABS.find((tab) => tab.key === activeTabKey)
  const { data: movies = [], isLoading, isError, error } = queriesByTab[activeTabKey]

  if (!movieId) return null

  return (
    <section id="movie-detail" className="recommendations-panel">
      <div className="container">
        <div className="section-heading">
          <span className="eyebrow">Recommended for this pick</span>
          <h2>{movieTitle ? `Because you picked “${movieTitle}”` : 'Recommendations'}</h2>
        </div>

        <div className="recommendations-panel__tabs">
          <div className="pill-tabs">
            {TABS.map((tab) => (
              <button
                key={tab.key}
                className={`pill-tab ${tab.key === activeTabKey ? 'is-active' : ''}`}
                onClick={() => setActiveTabKey(tab.key)}
              >
                {tab.label}
              </button>
            ))}
          </div>
          <p className="recommendations-panel__description">{activeTab.description}</p>
        </div>

        {isLoading && <p className="state-message">Finding recommendations…</p>}
        {isError && <p className="state-message">{error.message}</p>}

        {!isLoading && !isError && movies.length === 0 && (
          <p className="state-message">No related movies found for this pick yet.</p>
        )}

        {!isLoading && !isError && movies.length > 0 && (
          <div className="movie-grid">
            {movies.map((movie) => (
              <MovieCard
                key={movie.movie_id}
                movie={movie}
                matchPercent={movie[activeTab.scoreField] * 100}
                matchLabel={activeTab.matchLabel}
                onClick={() => onSelectMovie(movie)}
              />
            ))}
          </div>
        )}
      </div>
    </section>
  )
}
