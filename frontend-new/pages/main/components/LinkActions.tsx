import { useState, MouseEvent, FC, useCallback } from 'react'
import { Menu, MenuItem, IconButton, Box } from '@mui/material'
import { ThreeDots } from '../../../icons'

interface Props {
  onTransfer: () => void
  onDelete: () => void
}

export const LinkActions: FC<Props> = ({ onDelete, onTransfer }) => {
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
      <IconButton
        id='basic-button'
        aria-controls={open ? 'basic-menu' : undefined}
        aria-haspopup='true'
        aria-expanded={open ? 'true' : undefined}
        onClick={handleClick}
      >
        <ThreeDots />
      </IconButton>
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
