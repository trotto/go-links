import { Link, Box, Typography } from '@mui/material'
import { FC } from 'react'
import useSWR from 'swr'

import { TrottoLogo } from 'app/icons'
import { User } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

import { UserMenu } from './UserMenu'

interface AdminLink {
  text: string
  url: string
}

interface Props {
  user?: User
}

export const NavBar: FC<Props> = ({ user }) => {
  const { data: adminLinks } = useSWR(`/_admin_links`, fetcher<AdminLink[]>)
  return (
    <Box
      sx={{
        display: 'flex',
        height: '64px',
        backgroundColor: '#f6f8fa',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 24px',
        '@media (min-width: 840px)': {
          padding: ' 0 80px',
        },
      }}
    >
      <Link
        href='/'
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
        }}
      >
        <TrottoLogo />
        <Typography
          sx={{
            fontWeight: 500,
            fontSize: '20px',
            '@media (min-width: 840px)': {
              fontSize: '22px',
            },
            '@media (min-width: 1440px)': {
              fontSize: '24px',
            },
          }}
        >
          Trotto
        </Typography>
      </Link>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <Link className='item' href='/documentation' typography='h2'>
          Documentation
        </Link>
        {adminLinks?.map(({ url, text }) => (
          <Link className='item' href={url} key={url}>
            {text}
          </Link>
        ))}
        <Box sx={{ m: '0 12px' }}>{user && <UserMenu user={user} />}</Box>
      </Box>
    </Box>
  )
}
