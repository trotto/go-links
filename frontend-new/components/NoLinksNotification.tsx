import { Box, Typography } from '@mui/material'
import { FC } from 'react'

import { ArrowDown, NewLink } from 'app/icons'
import Background from 'app/public/new-link-background.svg'
import { media } from 'app/styles/theme'

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
        [media.TABLET]: {
          pb: 5,
          gap: 2,
        },
        [media.DESKTOP]: {
          pb: 6,
          mt: 2,
        },
      }}
    >
      <ArrowDown />
      <Box
        sx={{
          height: 8,
          [media.TABLET]: {
            height: 0,
          },
          [media.DESKTOP]: {
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
