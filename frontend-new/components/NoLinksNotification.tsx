import { Box, Typography } from '@mui/material'
import { FC } from 'react'

import { ArrowDown, NewLink } from 'app/icons'
import Background from 'app/public/new-link-background.svg'

export const NoLinksNotification: FC = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        borderRadius: '8px',
        flexDirection: 'column',
        alignItems: 'center',
        backgroundImage: `url(${Background.src})`,
        backgroundSize: 'cover',
        gap: '8px',
        pb: '32px',
        mt: '8px',
        '@media (min-width: 840px)': {
          pb: '40px',
          gap: '16px',
        },
        '@media (min-width: 1440px)': {
          pb: '48px',
          mt: '16px',
        },
      }}
    >
      <ArrowDown />
      <Box
        sx={{
          height: '8px',
          '@media (min-width: 840px)': {
            height: 0,
          },
          '@media (min-width: 1440px)': {
            height: '8px',
          },
        }}
      ></Box>
      <NewLink />
      <Typography
        sx={{
          color: '#fff',
        }}
        variant='h1'
      >
        Create a new go link!
      </Typography>
    </Box>
  )
}
