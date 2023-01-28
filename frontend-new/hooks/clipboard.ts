import { useCallback } from 'react'

export const useClipboard = (str?: string) => {
  return useCallback(() => str && navigator.clipboard.writeText(str), [str])
}
