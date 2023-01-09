import { Box, Typography, Link } from '@mui/material'

import { LinkIconButton } from 'app/components'
import { Google, Microsoft } from 'app/icons'
import { media } from 'app/styles/theme'

export default function Login() {
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
          href='/_/auth/login/google?redirect_to=https%3A%2F%2Ftrot.to'
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
          href='https://id.trot.to/sso/o365?redirect_to=https%3A%2F%2Ftrot.to'
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
          <Link href='/terms' sx={{ fontWeight: 600, color: '#343AAA' }}>
            Terms of Service
          </Link>{' '}
          and{' '}
          <Link href='/privacy' sx={{ fontWeight: 600, color: '#343AAA' }}>
            Privacy Policy.
          </Link>
        </Typography>
      </Box>
    </Box>
  )
}
