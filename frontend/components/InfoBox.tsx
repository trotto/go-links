import { Box } from '@mui/material'
import { BoxProps } from '@mui/system'
import { FC, PropsWithChildren } from 'react'

import { media } from 'app/styles/theme'

interface Props extends PropsWithChildren {
  sx?: BoxProps['sx']
  bold?: boolean
}

export const InfoBox: FC<Props> = ({ children, sx, bold = false }) => (
  <Box
    sx={{
      backgroundColor: '#fff',
      borderRadius: '32px',
      display: 'flex',
      alignItems: 'center',
      px: 1,
      height: 24,
      mr: 1,
      cursor: 'default',

      [media.TABLET]: {
        px: 2,
        mr: 3,
        height: 32,
      },
      ...sx,
    }}
  >
    <Box sx={{ textOverflow: 'ellipsis', overflow: 'hidden', typography: bold ? 'h3' : 'body1' }}>
      {children}
    </Box>
  </Box>
)
