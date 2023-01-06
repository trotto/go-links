import PersonIcon from '@mui/icons-material/Person'
import { Avatar, Box, IconButton, Menu, MenuItem, MenuItemProps, Link } from '@mui/material'
import { MouseEvent, useState, FC, PropsWithChildren } from 'react'

import { Vector, Burger } from 'app/icons'
import { media } from 'app/styles/theme'
import { User, AdminLink } from 'app/types'

interface Props {
  user: User
  adminLinks?: AdminLink[]
}

interface MLProps extends PropsWithChildren {
  sx?: MenuItemProps['sx']
  href?: string
}

const MenuLink: FC<MLProps> = ({ sx, children, href }) => (
  <MenuItem sx={{ pt: 1, pb: 1, px: 3, typography: 'body1', ...sx }}>
    <Link variant='body1' href={href} sx={{ color: '#343aaa' }}>
      {children}
    </Link>
  </MenuItem>
)

export const UserMenu: FC<Props> = ({ user, adminLinks }) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const open = Boolean(anchorEl)
  const handleClick = (event: MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }
  const handleClose = () => {
    setAnchorEl(null)
  }

  return (
    <>
      <Box
        sx={{
          display: 'none',
          [media.TABLET]: {
            display: 'flex',
            alignItems: 'center',
            textAlign: 'center',
            cursor: 'pointer',
          },
        }}
        onClick={handleClick}
      >
        <IconButton
          sx={{
            padding: 0,
            margin: 0,
          }}
          size='small'
          aria-controls={open ? 'account-menu' : undefined}
          aria-haspopup='true'
          aria-expanded={open ? 'true' : undefined}
        >
          <Avatar sx={{ width: 40, height: 40, backgroundColor: '#F27E8F' }}>
            <PersonIcon sx={{ fill: '#fff' }} />
          </Avatar>
        </IconButton>
        <Box sx={{ pl: 1, cursor: 'pointer' }}>
          <Vector />
        </Box>
      </Box>
      <Box
        sx={{
          display: 'flex',
          [media.TABLET]: {
            display: 'none',
          },
        }}
        onClick={handleClick}
      >
        <IconButton>
          <Burger />
        </IconButton>
      </Box>
      <Menu
        anchorEl={anchorEl}
        id='account-menu'
        open={open}
        onClose={handleClose}
        onClick={handleClose}
        PaperProps={{
          elevation: 0,
          sx: {
            overflow: 'visible',
            filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
            mt: 2,
            ml: '14px',
            right: 0,
            [media.TABLET]: {
              mt: 1.5,
              right: 'auto',
            },
            '& .MuiList-root': {
              padding: 0,
            },
            '& .MuiAvatar-root': {
              width: 32,
              height: 32,
              ml: -0.5,
              mr: 1,
            },
            '&:before': {
              content: '""',
              display: 'block',
              position: 'absolute',
              right: 26,
              top: 0,
              [media.TABLET]: {
                right: 14,
              },
              width: 10,
              height: 10,
              bgcolor: 'background.paper',
              transform: 'translateY(-50%) rotate(45deg)',
              zIndex: 0,
            },
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <Box
          sx={{
            '& .MuiMenuItem-root': {
              px: 3,
              color: '#343aaa',
              typography: 'body1',
            },
          }}
        >
          <MenuLink sx={{ pt: 3 }}>{user?.email}</MenuLink>
          <MenuLink href='/_/auth/logout' sx={{ pb: 3 }}>
            Sign Out
          </MenuLink>
        </Box>
        <Box
          sx={{
            display: 'block',

            [media.TABLET]: {
              display: 'none',
            },
          }}
        >
          <Box sx={{ mx: 3, border: '1px solid #343AAA' }}></Box>
          <MenuLink href='/documentation' sx={{ pt: 3 }}>
            Documentation
          </MenuLink>

          {adminLinks?.map(({ url, text }) => (
            <MenuLink href={url} key={url}>
              {text}
            </MenuLink>
          ))}

          <MenuLink href='https://github.com/trotto/go-links'>Github</MenuLink>
          <MenuLink href='/pricing'>Pricing</MenuLink>
          <MenuLink href='/privacy'>Privacy</MenuLink>
          <MenuLink href='/terms'>Terms</MenuLink>
          <MenuLink href='/contact' sx={{ pb: 3 }}>
            Contact us
          </MenuLink>
        </Box>
      </Menu>
    </>
  )
}
