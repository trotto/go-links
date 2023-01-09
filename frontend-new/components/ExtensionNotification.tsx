import { Box, Typography } from '@mui/material'
import { FC } from 'react'

import { LinkIconButton } from 'app/components/LinkIconButton'
import { Chrome } from 'app/icons'
import { media } from 'app/styles/theme'

export const ExtensionNotification: FC = () => {
  return (
    <Box
      sx={{
        p: 5,
        backgroundColor: '#FFBEA2',
        mb: 3,
        [media.TABLET]: {
          mb: 5,
        },
        color: '#fff',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2,
      }}
    >
      <Typography variant='h1'>Welcome! Let’s get started!</Typography>
      <Typography>
        Installing the Chrome extension is the best and easiest way to use go links. Install the
        extension now:
      </Typography>
      <LinkIconButton
        href='https://chrome.google.com/webstore/detail/trotto-go-links/nkeoojidblilnkcbbmfhaeebndapehjk'
        icon={<Chrome />}
      >
        Add the Chrome Extension
      </LinkIconButton>
    </Box>
  )
}
