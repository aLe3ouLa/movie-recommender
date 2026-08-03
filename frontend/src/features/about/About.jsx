import './about.css'

const TECHNIQUES = [
  {
    title: 'Content-Based',
    description:
      'TF-IDF over movie titles plus one-hot genre vectors, compared with cosine similarity — finds movies that read alike, independent of who watched them.',
  },
  {
    title: 'Collaborative Filtering',
    description:
      'Item-based ("audience also liked") from raw rating vectors, and user-based from mean-centered ratings across the 610 MovieLens viewers — finds patterns in taste, not text.',
  },
  {
    title: 'Hybrid Ranking',
    description:
      'Blends content similarity (55%), collaborative similarity (30%), and a Bayesian-weighted rating (15%) into one ranked list.',
  },
]

export function About() {
  return (
    <section id="about" className="about">
      <div className="container">
        <div className="section-heading">
          <span className="eyebrow">Built to Learn ML Systems</span>
          <h2>Three recommendation models, one dataset</h2>
          <p>
            This is a study project for learning how recommender systems are actually
            built and served — not a commercial product. Every score on this page comes
            from one of the models below, running against the public MovieLens
            ml-latest-small dataset.
          </p>
        </div>

        <div className="about__grid">
          {TECHNIQUES.map((technique) => (
            <div key={technique.title} className="about__card">
              <h3>{technique.title}</h3>
              <p>{technique.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
