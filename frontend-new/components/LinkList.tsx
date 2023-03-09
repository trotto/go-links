import { Box } from '@mui/material'
import { FC, useRef, useEffect, useState, useMemo } from 'react'

import { Link } from 'app/types'

import { LinkItem } from './LinkItem'

interface Props {
  links?: Link[]
}

export const LinkList: FC<Props> = ({ links }) => {
  const ref = useRef<HTMLDivElement>(null)
  const [overflowed, setOverflowed] = useState(false)

  useEffect(
    () => setOverflowed((ref.current?.clientHeight || 0) - (ref.current?.scrollHeight || 0) < 0),
    [ref, links],
  )

  const displayLinks = useMemo(
    () => links?.sort((a, b) => b.visits_count - a.visits_count),
    [links],
  )

  return (
    <Box
      sx={{
        overflow: 'scroll',
        backgroundColor: '#f6f8fa',
        '&::-webkit-scrollbar': {
          display: 'none',
        },
        ...(overflowed
          ? {
              boxShadow: 'rgb(0 0 0 / 20%) 0 9px 9px -9px inset',
              // boxShadow: 'inset 0px 4px 8px rgba(0, 0, 0, 0.2)',
              // borderWidth: '1px 1px 0px 1px',
              // borderStyle: 'solid',
              // borderColor: '#A3A3A3',
            }
          : {}),
      }}
      ref={ref}
    >
      {displayLinks?.map((link) => (
        <LinkItem key={link.id} link={link} />
      ))}
    </Box>
  )
}
