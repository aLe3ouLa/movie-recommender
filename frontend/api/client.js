const API_URL =
  import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000'

export async function apiRequest(path, { signal } = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    signal,
  })

  if (!response.ok) {
    const body = await response.json().catch(() => null)

    throw new Error(
      body?.detail ?? `Request failed with status ${response.status}`,
    )
  }

  return response.json()
}