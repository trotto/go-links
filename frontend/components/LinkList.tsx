import { Box, useMediaQuery } from '@mui/material'
import { useVirtual } from '@tanstack/react-virtual'
import { range } from 'lodash'
import { FC, useRef, useEffect, useState, useMemo, useCallback } from 'react'

import { media } from 'app/styles/theme'
import { Link } from 'app/types'

import { LinkItem, LinkItemDummy } from './LinkItem'

interface Props {
  links?: Link[]
  isLoading: boolean
}

export const LinkList: FC<Props> = ({ links, isLoading = false }) => {
  const ref = useRef<HTMLDivElement>(null)
  const [overflowed, setOverflowed] = useState(false)
  const isTablet = useMediaQuery(media.TABLET)
  const isDesktop = useMediaQuery(media.DESKTOP)

  const rowHeight = useMemo(() => {
    if (isTablet) {
      return 133
    }

    if (isDesktop) {
      return 141
    }

    return 97
  }, [isTablet, isDesktop])

  const renderRow = useCallback(
    ({ index }: { index: number }) =>
      links && <LinkItem key={links[index].id} link={links[index]} />,
    [links],
  )

  useEffect(() => {
    setOverflowed((ref.current?.clientHeight || 0) - rowHeight * (links?.length || 0) < 0)
  }, [ref, links, rowHeight])

  const rows = useVirtual({
    size: links?.length || 0,
    parentRef: ref,
    overscan: 10,
    estimateSize: useCallback(() => rowHeight, [rowHeight]),
  })

  return (
    <Box
      sx={{
        overflow: 'scroll',
        backgroundColor: '#f6f8fa',
        '&::-webkit-scrollbar': {
          display: 'none',
        },
        ...(overflowed || isLoading
          ? {
              boxShadow: 'rgb(0 0 0 / 20%) 0 9px 9px -9px inset',
            }
          : {}),
      }}
      ref={ref}
    >
      {isLoading
        ? range(0, 10).map((index) => <LinkItemDummy key={index}></LinkItemDummy>)
        : rows.virtualItems.map(renderRow)}
    </Box>
  )
}
