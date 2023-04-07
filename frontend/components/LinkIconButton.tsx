import { Box, Button, ButtonProps } from '@mui/material'
import { FC, ReactNode, PropsWithChildren, HTMLAttributeAnchorTarget } from 'react'

import { media } from 'app/styles/theme'

interface Props extends PropsWithChildren {
  href?: string
  icon: ReactNode
  sx?: ButtonProps['sx']
  target?: HTMLAttributeAnchorTarget
}

export const LinkIconButton: FC<Props> = ({ href = '#', icon, children, sx, ...props }) => {
  return (
    <Button
      href={href}
      {...props}
      sx={{
        backgroundColor: '#FB815B',
        height: 48,
        pr: 1,
        pl: 0.5,
        typography: 'h2',

        '&:hover': {
          backgroundColor: '#C5443C;',
        },

        [media.TABLET]: {
          pr: 2,
          height: 56,
        },
        [media.DESKTOP]: {
          height: 64,
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
