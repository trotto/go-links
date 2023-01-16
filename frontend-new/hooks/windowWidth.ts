import { useState, useEffect, useMemo } from 'react'

export enum ScreenType {
  MOBILE = 0,
  TABLET = 840,
  DESKTOP = 1440,
}

export const useWindowWidth = () => {
  const [width, setWidth] = useState<number>()

  useEffect(() => {
    function handleResize() {
      const { innerWidth } = window
      setWidth(innerWidth)
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const isMobile = useMemo(() => !width || width < ScreenType.TABLET, [width])

  return { width, isMobile }
}
