import { Box, Link } from '@mui/material'
import { FC } from 'react'

import { GithubLogo } from 'app/icons'

export const Footer: FC = () => {
  return (
    <Box
      sx={{
        display: 'none',
        '@media (min-width: 839px)': {
          height: '64px',
          display: 'flex',
        },
        backgroundColor: '#f6f8fa',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '24px',
      }}
    >
      <Link href='https://github.com/trotto/go-links'>
        <GithubLogo />
      </Link>
      <Link href={'/pricing'}>Pricing</Link>
      <Link href={'/privacy'}>Privacy</Link>
      <Link href={'/terms'}>Terms</Link>
      <Link href={'/contact'}>Contact us</Link>
    </Box>
  )
}
