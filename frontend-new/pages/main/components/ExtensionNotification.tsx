import { Box, Typography, Button } from '@mui/material'
import { FC } from 'react'

import { Chrome } from 'app/icons'

export const ExtensionNotification: FC = () => {
  return (
    <Box
      sx={{
        p: '40px',
        backgroundColor: '#FFBEA2',
        mb: '24px',
        '@media (min-width: 839px)': {
          mb: '40px',
        },
        color: '#fff',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '16px',
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
          height: '64px',
          pl: '4px',
          pr: '16px',
          '&:hover': {
            backgroundColor: '#FFBBC5',
          },
        }}
      >
        <Box
          sx={{
            width: '56px',
            height: '56px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#fff',
            borderRadius: '32px',
            mr: '16px',
          }}
        >
          <Chrome />
        </Box>
        Add the Chrome Extension
      </Button>
    </Box>
  )
}
