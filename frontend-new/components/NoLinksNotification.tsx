import { Box, Typography } from '@mui/material'
import { FC } from 'react'

import { ArrowDown, NewLink } from 'app/icons'
import Background from 'app/public/new-link-background.svg'

export const NoLinksNotification: FC = () => {
  return (
    <Box
      sx={{
        height: '248px',
        display: 'flex',
        borderRadius: '8px',
        flexDirection: 'column',
        alignItems: 'center',
        backgroundImage: `url(${Background.src})`,
        backgroundSize: 'cover',
        gap: '16px',
        pb: '48px',
        mb: '40px',
      }}
    >
      <ArrowDown />
      <NewLink />
      <Typography
        sx={{
          color: '#fff',
          fontSize: '24px',
          fontWeight: 700,
        }}
        variant='h1'
      >
        Create a new go link!
      </Typography>
    </Box>
  )
}
