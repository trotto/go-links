import PersonIcon from '@mui/icons-material/Person'
import { Avatar, Box, IconButton, Menu, MenuItem } from '@mui/material'
import { Vector } from 'icons'
import { FC } from 'react'
import { MouseEvent, useState } from 'react'
import { User } from 'types'

interface Props {
  user: User
}

export const UserMenu: FC<Props> = ({ user }) => {
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
        sx={{ display: 'flex', alignItems: 'center', textAlign: 'center', cursor: 'pointer' }}
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
            <PersonIcon />
          </Avatar>
        </IconButton>
        <Box sx={{ pl: '8px', cursor: 'pointer' }}>
          <Vector />
        </Box>
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
            mt: 1.5,
            ml: '14px',
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
              top: 0,
              right: 14,
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
        <MenuItem sx={{ fontSize: '14px', color: '#343aaa', padding: '24px 24px 8px' }}>
          {user?.email}
        </MenuItem>
        <MenuItem sx={{ fontSize: '14px', color: '#343aaa', padding: '8px 24px 24px' }}>
          <a href='/_/auth/logout' style={{ color: '#343aaa' }}>
            Sign Out
          </a>
        </MenuItem>
      </Menu>
    </>
  )
}
