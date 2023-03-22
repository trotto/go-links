import PersonIcon from '@mui/icons-material/Person'
import { Avatar, Box, IconButton, Menu, MenuItem, MenuItemProps, Link } from '@mui/material'
import { MouseEvent, useState, FC, PropsWithChildren, useContext, useMemo } from 'react'

import { navigationLinks } from 'app/config'
import { Context } from 'app/context'
import { Vector, Burger } from 'app/icons'
import { media } from 'app/styles/theme'
import { AdminLink } from 'app/types'

interface Props {
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

export const UserMenu: FC<Props> = ({ adminLinks }) => {
  const { user } = useContext(Context)
  const feedbackLink = useMemo(() => user && navigationLinks.SHARE_FEEDBACK(user.email), [user])

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
            py: 2,
            '& .MuiMenuItem-root': {
              px: 3,
              color: '#343aaa',
              typography: 'body1',
            },
          }}
        >
          <Box sx={{ pt: 1, pb: 1, px: 3, typography: 'body1', color: '#343aaa' }}>
            {user?.email}
          </Box>
          <MenuLink href={navigationLinks.LOGOUT}>Sign Out</MenuLink>
        </Box>
        <Box
          sx={{
            display: 'block',
            pb: 2,

            [media.TABLET]: {
              display: 'none',
            },
          }}
        >
          <Box sx={{ mx: 3, border: '1px solid #343AAA', mb: 2 }}></Box>
          <MenuLink href={navigationLinks.DOCUMENTATION}>Documentation</MenuLink>

          {adminLinks?.map(({ url, text }) => (
            <MenuLink href={url} key={url}>
              {text}
            </MenuLink>
          ))}

          <MenuLink href={navigationLinks.GITHUB}>Github</MenuLink>
          <MenuLink href={navigationLinks.PRICING}>Pricing</MenuLink>
          <MenuLink href={navigationLinks.PRIVACY}>Privacy</MenuLink>
          <MenuLink href={navigationLinks.TERMS}>Terms</MenuLink>
          <MenuLink href={navigationLinks.CONTACT}>Contact us</MenuLink>
          <MenuLink href={feedbackLink}>Share feedback</MenuLink>
        </Box>
      </Menu>
    </>
  )
}
