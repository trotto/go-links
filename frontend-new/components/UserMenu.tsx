import { FC } from 'react'
import styled from '@emotion/styled'
import { useState, MouseEvent } from 'react'
import Box from '@mui/material/Box'
import Avatar from '@mui/material/Avatar'
import Menu from '@mui/material/Menu'
import MenuItem from '@mui/material/MenuItem'
import IconButton from '@mui/material/IconButton'
import useSWR from 'swr'
import { fetcher } from '../utils/fetcher'
import PersonIcon from '@mui/icons-material/Person'
import { Vector } from '../icons'

const StyledDiv = styled.div`
  .vector {
    padding-left: 8px;
    cursor: pointer;
  }

  a {
  }
`

interface User {
  admin: boolean
  created: string
  email: string
  id: number
  info_bar?: any
  keywords_validation_regex: string
  notifications: any
  org_edit_mode: string
  organization: string
  read_only_mode?: any
  role?: any
}

export const UserMenu: FC = () => {
  const { data: user } = useSWR(`/_/api/users/me`, fetcher<User>)
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const open = Boolean(anchorEl)
  const handleClick = (event: MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }
  const handleClose = () => {
    setAnchorEl(null)
  }

  return (
    <StyledDiv>
      <Box
        sx={{ display: 'flex', alignItems: 'center', textAlign: 'center', cursor: 'pointer' }}
        onClick={handleClick}
      >
        <IconButton
          sx={{
            padding: 0,
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
        <div className='vector'>
          <Vector />
        </div>
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
    </StyledDiv>
  )
}
