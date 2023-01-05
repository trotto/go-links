import { useState, useCallback } from 'react'

export const useModal: () => [boolean, () => void, () => void] = () => {
  const [isOpen, setIsOpen] = useState(false)
  const onOpen = useCallback(() => setIsOpen(true), [setIsOpen])
  const onClose = useCallback(() => setIsOpen(false), [setIsOpen])

  return [isOpen, onOpen, onClose]
}
