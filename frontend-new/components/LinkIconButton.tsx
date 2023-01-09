import { Box, Button, ButtonProps } from '@mui/material'
import { FC, ReactNode, PropsWithChildren } from 'react'

import { media } from 'app/styles/theme'

interface Props extends PropsWithChildren {
  href?: string
  icon: ReactNode
  sx?: ButtonProps['sx']
}

export const LinkIconButton: FC<Props> = ({ href = '#', icon, children, sx }) => {
  return (
    <Button
      href={href}
      target='_blank'
      sx={{
        backgroundColor: '#FB815B',
        height: 48,
        pr: 1,
        [media.TABLET]: {
          pr: 2,
          height: 56,
        },
        [media.DESKTOP]: {
          height: 64,
        },
        pl: 0.5,
        typography: 'h2',
        '&:hover': {
          backgroundColor: '#C5443C;',
        },
        ...sx,
      }}
    >
      <Box
        sx={{
          width: 40,
          height: 40,
          mr: 1,
          [media.TABLET]: {
            mr: 2,
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
        }}
      >
        {icon}
      </Box>
      {children}
    </Button>
  )
}
