import { useState } from 'react'
import { Navbar } from './layout/navbar/Navbar'
import { Footer } from './layout/footer/Footer'
import { Hero } from './features/landingpage/Hero'
import { PopularGrid } from './features/movies/PopularGrid'
import { RecommendationsPanel } from './features/movies/RecommendationsPanel'
import { GenrePicker } from './features/movies/GenrePicker'
import { PredictedScore } from './features/movies/PredictedScore'
import { About } from './features/about/About'
import { useViewerId } from './features/user/useViewerId'
import './App.css'

function App() {
  const [selectedMovie, setSelectedMovie] = useState(null)
  const [viewerId, setViewerId] = useViewerId()

  function handleSelectMovie(movie) {
    setSelectedMovie(movie)

    requestAnimationFrame(() => {
      document.getElementById('movie-detail')?.scrollIntoView({ behavior: 'smooth' })
    })
  }

  return (
    <main>
      <Navbar onSelectMovie={handleSelectMovie} viewerId={viewerId} onViewerIdChange={setViewerId} />

      <Hero />

      <PopularGrid onSelectMovie={handleSelectMovie} />

      {selectedMovie && (
        <RecommendationsPanel
          movieId={selectedMovie.movie_id}
          movieTitle={selectedMovie.title}
          onSelectMovie={handleSelectMovie}
        />
      )}

      <GenrePicker onSelectMovie={handleSelectMovie} />

      <PredictedScore viewerId={viewerId} onViewerIdChange={setViewerId} />

      <About />

      <Footer />
    </main>
  )
}

export default App
