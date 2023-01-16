import CloseRoundedIcon from '@mui/icons-material/CloseRounded'
import { Box, Typography, IconButton } from '@mui/material'
import { FC } from 'react'

import { LinkIconButton } from 'app/components/LinkIconButton'
import { useDismissExtensionNotification, useGetMe } from 'app/hooks'
import { Chrome } from 'app/icons'
import { media } from 'app/styles/theme'

export const ExtensionNotification: FC = () => {
  const handleClose = useDismissExtensionNotification()
  const { user, isLoading } = useGetMe()

  if (isLoading || user?.notifications?.install_extension === 'dismissed') {
    return <></>
  }
  return (
    <Box
      sx={{
        display: 'none',
        position: 'relative',
        p: 5,
        backgroundColor: '#FFBEA2',
        mb: 3,
        [media.TABLET]: {
          display: 'flex',
          mb: 5,
        },
        borderRadius: '8px',
        color: '#fff',
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
      <IconButton
        sx={{
          position: 'absolute',
          m: 2,
          right: 0,
          top: 0,
        }}
        onClick={handleClose}
      >
        <CloseRoundedIcon sx={{ fill: '#fff' }} />
      </IconButton>
    </Box>
  )
}
