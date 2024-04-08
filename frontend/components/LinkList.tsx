import { Box, useMediaQuery } from '@mui/material'
import { range } from 'lodash'
import { FC, useRef, useEffect, useState, useMemo, useCallback } from 'react'
import AutoSizer from 'react-virtualized/dist/commonjs/AutoSizer'
import List, { ListRowRenderer } from 'react-virtualized/dist/commonjs/List'

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

  const renderRow: ListRowRenderer = useCallback(
    ({ index, style }) =>
      links && (
        <Box
          style={style}
          key={links[index].id}
          sx={{ backgroundColor: !overflowed ? '#f6f8fa' : 'transparent' }}
        >
          <LinkItem link={links[index]} />
        </Box>
      ),
    [links, overflowed],
  )

  useEffect(() => {
    setOverflowed((ref.current?.clientHeight || 0) - rowHeight * (links?.length || 0) < 0)
  }, [ref, links, rowHeight])

  return (
    <Box
      sx={{
        height: '100%',
        '& .ReactVirtualized__List': {
          '&::-webkit-scrollbar': {
            display: 'none',
          },
        },
        ...(overflowed || isLoading
          ? {
              boxShadow: 'rgb(0 0 0 / 20%) 0 9px 9px -9px inset',
              backgroundColor: '#f6f8fa',
            }
          : {}),
      }}
      ref={ref}
    >
      {isLoading ? (
        range(0, 10).map((index) => <LinkItemDummy key={index}></LinkItemDummy>)
      ) : (
        <AutoSizer>
          {({ width, height }) => (
            <List
              width={width}
              height={height}
              rowHeight={rowHeight}
              rowRenderer={renderRow}
              rowCount={links?.length || 0}
              overscanRowCount={10}
            />
          )}
        </AutoSizer>
      )}
    </Box>
  )
}
