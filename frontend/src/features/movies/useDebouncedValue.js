import { useEffect, useMemo, useState } from 'react'
import debounce from 'lodash/debounce'

export function useDebouncedValue(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value)

  const updateValue = useMemo(
    () => debounce(setDebouncedValue, delay),
    [delay],
  )

  useEffect(() => {
    updateValue(value)

    return () => {
      updateValue.cancel()
    }
  }, [value, updateValue])

  return debouncedValue
}