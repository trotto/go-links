import { Link, Box, Typography } from '@mui/material'
import { FC } from 'react'

import { useGetAdminLinks } from 'app/hooks'
import { TrottoLogo } from 'app/icons'
import { media } from 'app/styles/theme'
import { User } from 'app/types'

import { UserMenu } from './UserMenu'

interface Props {
  user?: User
}

export const NavBar: FC<Props> = ({ user }) => {
  const { adminLinks } = useGetAdminLinks()
  return (
    <Box
      sx={{
        display: 'flex',
        flexShrink: 0,
        height: 48,
        backgroundColor: '#f6f8fa',
        justifyContent: 'space-between',
        alignItems: 'center',
        px: 3,
        [media.TABLET]: {
          px: 10,
          height: 64,
        },
      }}
    >
      <Link
        href='/'
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 1,
        }}
      >
        <TrottoLogo />
        <Typography
          sx={{
            fontWeight: 500,
            fontSize: '20px',
            [media.TABLET]: {
              fontSize: '22px',
            },
            [media.DESKTOP]: {
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
          gap: 3,
        }}
      >
        <Box
          sx={{
            display: 'none',
            gap: 3,
            [media.TABLET]: {
              display: 'flex',
              alignItems: 'center',
            },
          }}
        >
          <Link href='/documentation' typography='h2' sx={{ fontWeight: 400 }}>
            Documentation
          </Link>
          {adminLinks?.map(({ url, text }) => (
            <Link href={url} key={url}>
              {text}
            </Link>
          ))}
        </Box>
        <Box>{user && <UserMenu user={user} adminLinks={adminLinks} />}</Box>
      </Box>
    </Box>
  )
}
