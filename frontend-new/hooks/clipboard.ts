import { useCallback } from 'react'

export const useClipboard = (str: string) => {
  return useCallback(() => navigator.clipboard.writeText(str), [str])
}
