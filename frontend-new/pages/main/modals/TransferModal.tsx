import { FC, useCallback } from 'react'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Modal from '@mui/material/Modal'
import { Link } from '../../../types'
import TextField from '@mui/material/TextField'
import useSWR from 'swr'
import { fetcher } from '../../../utils/fetcher'

const style = {
  position: 'absolute' as const,
  display: 'flex',
  'flex-direction': 'column',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
}

interface Props {
  open: boolean
  onClose: () => void
  link: Link
}

interface TransferToken {
  url: string
}

export const TransferModal: FC<Props> = ({ open, onClose, link }) => {
  const { namespace, shortpath, id } = link
  const { data: transferToken } = useSWR(`/_/api/links/${id}/transfer_link`, (url) =>
    fetcher<TransferToken>(url, { method: 'POST' }),
  )

  const handleCopy = useCallback(
    () => transferToken && navigator.clipboard.writeText(transferToken.url),
    [transferToken],
  )

  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby='modal-modal-title'
      aria-describedby='modal-modal-description'
    >
      <Box sx={style}>
        <p>
          To transfer ownership of{' '}
          <b>
            {namespace}/{shortpath}
          </b>
          , copy this link and send it to the new owner
        </p>
        <TextField value={transferToken?.url} multiline></TextField>
        <div>
          <Button variant='contained' onClick={handleCopy}>
            Click to copy
          </Button>
          <Button variant='contained' onClick={onClose}>
            Done
          </Button>
        </div>
      </Box>
    </Modal>
  )
}
