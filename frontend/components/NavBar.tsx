import { Link, Box, Typography } from '@mui/material'
import { FC, useContext } from 'react'

import { navigationLinks } from 'app/config'
import { Context } from 'app/context'
import { useGetAdminLinks } from 'app/hooks'
import { TrottoLogo } from 'app/icons'
import { media } from 'app/styles/theme'

import { UserMenu } from './UserMenu'

export const NavBar: FC = () => {
  const { user } = useContext(Context)

  const { adminLinks } = useGetAdminLinks()
  return (
    <Box
      sx={{
        display: 'flex',
        flexShrink: 0,
        height: 48,
        backgroundColor: '#f6f8fa',
        justifyContent: user ? 'space-between' : 'center',
        alignItems: 'center',
        px: 3,
        [media.TABLET]: {
          px: 10,
          height: 64,
        },
      }}
    >
      <Link
        href={navigationLinks.ROOT}
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
      {!!user && (
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
            <Link
              href={navigationLinks.DOCUMENTATION}
              typography='h2'
              sx={{ fontWeight: 400 }}
              target='_blank'
            >
              Documentation
            </Link>
            {adminLinks?.map(({ url, text }) => (
              <Link href={url} key={url} target='_blank' typography='h2' sx={{ fontWeight: 400 }}>
                {text}
              </Link>
            ))}
          </Box>
          <Box>
            <UserMenu adminLinks={adminLinks} />
          </Box>
        </Box>
      )}
    </Box>
  )
}
