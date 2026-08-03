import './footer.css'

const COLUMNS = [
  {
    heading: 'Discover',
    links: ['Popular Right Now', 'Browse by Genre', 'Search Movies'],
  },
  {
    heading: 'Recommendation Modes',
    links: ['Hybrid Picks', 'Similar Content', 'Audience Also Liked', 'Personalized for You'],
  },
]

export function Footer() {
  return (
    <footer className="footer">
      <div className="container footer__inner">
        <div className="footer__columns">
          {COLUMNS.map((column) => (
            <div key={column.heading} className="footer__column">
              <h3>{column.heading}</h3>
              <ul>
                {column.links.map((link) => (
                  <li key={link}>{link}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="footer__brand">
          <p>
            🍿 <strong>Popcorn Picks</strong>
          </p>
          <p>
            A study project exploring recommender systems with FastAPI, scikit-learn, and
            React.
          </p>
          <p className="footer__attribution">
            Ratings data from{' '}
            <a href="https://grouplens.org/datasets/movielens/" target="_blank" rel="noreferrer">
              MovieLens
            </a>{' '}
            (GroupLens Research). Poster images from{' '}
            <a href="https://www.themoviedb.org/" target="_blank" rel="noreferrer">
              TMDB
            </a>
            . This product uses the TMDB API but is not endorsed or certified by TMDB.
          </p>
        </div>
      </div>
    </footer>
  )
}
