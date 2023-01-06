import { Box, Typography, Button } from '@mui/material'
import { FC } from 'react'

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
      <Button
        href='https://chrome.google.com/webstore/detail/trotto-go-links/nkeoojidblilnkcbbmfhaeebndapehjk'
        target='_blank'
        sx={{
          backgroundColor: '#FB815B',
          height: 48,
          [media.TABLET]: {
            height: 56,
          },
          [media.DESKTOP]: {
            height: 64,
          },
          pl: 0.5,
          pr: 2,
          typography: 'h2',
          '&:hover': {
            backgroundColor: '#FFBBC5',
          },
        }}
      >
        <Box
          sx={{
            width: 40,
            height: 40,
            [media.TABLET]: {
              width: 48,
              height: 48,
            },
            [media.DESKTOP]: {
              width: 56,
              height: 56,
            },
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#fff',
            borderRadius: '32px',
            mr: 2,
          }}
        >
          <Chrome />
        </Box>
        Add the Chrome Extension
      </Button>
    </Box>
  )
}