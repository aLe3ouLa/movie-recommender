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
    enabled: movieId !== null || movieId !== undefined,
  })
}