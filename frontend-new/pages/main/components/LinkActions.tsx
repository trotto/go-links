import { Box, IconButton, Menu, MenuItem, Tooltip } from '@mui/material'
import { FC, MouseEvent, useCallback, useState } from 'react'

import { ThreeDots } from 'app/icons'

interface Props {
  onTransfer: () => void
  onDelete: () => void
  disabled: boolean
}

export const LinkActions: FC<Props> = ({ onDelete, onTransfer, disabled }) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const open = Boolean(anchorEl)
  const handleClick = (event: MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget)
  }
  const handleClose = () => {
    setAnchorEl(null)
  }

  const handleDelete = useCallback(() => {
    onDelete()
    handleClose()
  }, [onDelete, handleClose])

  const handleTransfer = useCallback(() => {
    onTransfer()
    handleClose()
  }, [onTransfer, handleClose])

  return (
    <Box sx={{ display: 'inline-flex' }}>
      <Tooltip title={disabled && 'You don’t have permission to modify this go link'}>
        <span>
          <IconButton
            id='basic-button'
            aria-controls={open ? 'basic-menu' : undefined}
            aria-haspopup='true'
            aria-expanded={open ? 'true' : undefined}
            onClick={handleClick}
            disabled={disabled}
            sx={{
              '&:disabled': {
                opacity: 0.1,
              },
            }}
          >
            <ThreeDots />
          </IconButton>
        </span>
      </Tooltip>
      <Menu
        id='basic-menu'
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
      >
        <MenuItem onClick={handleTransfer}>Transfer</MenuItem>
        <MenuItem onClick={handleDelete}>Delete</MenuItem>
      </Menu>
    </Box>
  )
}
