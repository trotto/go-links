import { Box, Typography, Link } from '@mui/material'
import { FC } from 'react'

import { LinkIconButton } from 'app/components'
import { navigationLinks } from 'app/config'
import { Google, Microsoft } from 'app/icons'
import { media } from 'app/styles/theme'

export const LoginPage: FC = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
      }}
    >
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          flexDirection: 'column',
          backgroundColor: '#F4F3FF',
          gap: 3,
          color: '#343AAA',

          width: 276,
          height: 276,
          mt: 4,
          px: 5.5,

          [media.TABLET]: {
            mt: 8,
            width: 379,
            height: 352,
            px: 9,
          },

          [media.DESKTOP]: {
            mt: 8,
            width: 432,
            height: 436,
            px: 10.5,
          },
        }}
      >
        <Typography variant='h1'>Sign In</Typography>
        <LinkIconButton
          icon={<Google />}
          href={navigationLinks.LOGIN_GOOGLE}
          sx={{
            backgroundColor: '#646AE7',
            '&:hover': {
              backgroundColor: '#343AAA',
            },
          }}
        >
          Sign in with Google
        </LinkIconButton>
        <LinkIconButton
          icon={<Microsoft />}
          href={navigationLinks.LOGIN_MICROSOFT}
          sx={{
            backgroundColor: '#646AE7',
            '&:hover': {
              backgroundColor: '#343AAA',
            },
          }}
        >
          Sign in with Microsoft
        </LinkIconButton>
        <Typography>
          By signing in, you agree to Trotto&apos;s{' '}
          <Link href={navigationLinks.TERMS} sx={{ fontWeight: 600, color: '#343AAA' }}>
            Terms of Service
          </Link>{' '}
          and{' '}
          <Link href={navigationLinks.PRIVACY} sx={{ fontWeight: 600, color: '#343AAA' }}>
            Privacy Policy.
          </Link>
        </Typography>
      </Box>
    </Box>
  )
}
