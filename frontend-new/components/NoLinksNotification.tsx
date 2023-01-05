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
        gap: 1,
        pb: 4,
        mt: 1,
        '@media (min-width: 840px)': {
          pb: 5,
          gap: 2,
        },
        '@media (min-width: 1440px)': {
          pb: 6,
          mt: 2,
        },
      }}
    >
      <ArrowDown />
      <Box
        sx={{
          height: 8,
          '@media (min-width: 840px)': {
            height: 0,
          },
          '@media (min-width: 1440px)': {
            height: 8,
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
