import { Box, Link } from '@mui/material'
import { FC } from 'react'

import { GithubLogo } from 'app/icons'
import { media } from 'app/styles/theme'
import { navigationLinks } from 'app/config'

export const Footer: FC = () => {
  return (
    <Box
      sx={{
        boxShadow: '0px -1px 4px rgba(0, 0, 0, 0.1)',
        display: 'none',
        flexShrink: 0,
        backgroundColor: '#f6f8fa',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 3,

        [media.TABLET]: {
          height: 64,
          display: 'flex',
        },
      }}
    >
      <Link href={navigationLinks.GITHUB}>
        <GithubLogo />
      </Link>
      <Link href={navigationLinks.PRICING}>Pricing</Link>
      <Link href={navigationLinks.PRIVACY}>Privacy</Link>
      <Link href={navigationLinks.TERMS}>Terms</Link>
      <Link href={navigationLinks.CONTACT}>Contact us</Link>
    </Box>
  )
}
