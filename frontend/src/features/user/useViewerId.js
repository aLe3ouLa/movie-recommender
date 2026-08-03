import { useEffect, useState } from 'react'

const STORAGE_KEY = 'popcorn-picks:viewer-id'

export function useViewerId() {
  const [viewerId, setViewerId] = useState(
    () => localStorage.getItem(STORAGE_KEY) ?? '',
  )

  useEffect(() => {
    if (viewerId) {
      localStorage.setItem(STORAGE_KEY, viewerId)
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  }, [viewerId])

  return [viewerId, setViewerId]
}
