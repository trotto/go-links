import { Box, Link } from '@mui/material'
import { FC } from 'react'

import { GithubLogo } from 'app/icons'
import { media } from 'app/styles/theme'

export const Footer: FC = () => {
  return (
    <Box
      sx={{
        boxShadow: '0px -1px 4px rgba(0, 0, 0, 0.1)',
        display: 'none',
        flexShrink: 0,
        [media.TABLET]: {
          height: 64,
          display: 'flex',
        },
        backgroundColor: '#f6f8fa',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 3,
      }}
    >
      <Link href='https://github.com/trotto/go-links'>
        <GithubLogo />
      </Link>
      <Link href='/pricing'>Pricing</Link>
      <Link href='/privacy'>Privacy</Link>
      <Link href='/terms'>Terms</Link>
      <Link href='/contact'>Contact us</Link>
    </Box>
  )
}
