import { useRepositoryQuery } from '../../../api/useRepositoryQuery'

export function useMovieSearch(query) {
  const normalizedQuery = query.trim()

  return useRepositoryQuery({
    queryKey: ['movies', 'search', normalizedQuery],
    path: '/movies/search',
    params: {
      query: normalizedQuery,
    },
    enabled: normalizedQuery.length >= 2,
  })
}

export function useMovieRecommendations(movieId) {
  return useRepositoryQuery({
    queryKey: ['movies', movieId, 'recommendations'],
    path: `/movies/${movieId}/recommendations`,
    enabled: movieId !== null && movieId !== undefined,
  })
}

export function useSimilarMovies(movieId) {
  return useRepositoryQuery({
    queryKey: ['movies', movieId, 'similar'],
    path: `/movies/${movieId}/similar`,
    enabled: movieId !== null && movieId !== undefined,
  })
}

export function useAudienceAlsoLiked(movieId) {
  return useRepositoryQuery({
    queryKey: ['movies', movieId, 'audience-also-liked'],
    path: `/movies/${movieId}/audience-also-liked`,
    enabled: movieId !== null && movieId !== undefined,
  })
}

export function usePopularMovies(limit = 10) {
  return useRepositoryQuery({
    queryKey: ['movies', 'popular', limit],
    path: '/movies/popular',
    params: { limit },
  })
}

export function useGenres() {
  return useRepositoryQuery({
    queryKey: ['movies', 'genres'],
    path: '/movies/genres',
  })
}

export function useMoviesByGenre(genre, limit = 10) {
  return useRepositoryQuery({
    queryKey: ['movies', 'genre', genre, limit],
    path: `/movies/genre/${encodeURIComponent(genre)}`,
    params: { limit },
    enabled: Boolean(genre),
  })
}

export function useUserRecommendations(userId, limit = 10) {
  return useRepositoryQuery({
    queryKey: ['users', userId, 'recommendations', limit],
    path: `/users/${userId}/recommendations`,
    params: { limit },
    enabled: Boolean(userId),
  })
}