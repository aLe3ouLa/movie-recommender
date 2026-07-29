import { useQuery } from '@tanstack/react-query'

import { apiRequest } from './client'

function createPath(path, params) {
  const searchParams = new URLSearchParams()

  for (const [key, value] of Object.entries(params ?? {})) {
    if (value !== undefined && value !== null && value !== '') {
      searchParams.set(key, String(value))
    }
  }

  const queryString = searchParams.toString()

  return queryString ? `${path}?${queryString}` : path
}

export function useRepositoryQuery({
  queryKey,
  path,
  params,
  enabled = true,
  ...queryOptions
}) {
  return useQuery({
    ...queryOptions,
    queryKey,
    enabled,
    queryFn: ({ signal }) => {
      const requestPath = createPath(path, params)

      return apiRequest(requestPath, { signal })
    },
  })
}