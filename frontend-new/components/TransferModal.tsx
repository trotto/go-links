import { Typography } from '@mui/material'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import { FC } from 'react'

import { useGetTransferToken, useClipboard, useFullShortPath } from 'app/hooks'
import { media } from 'app/styles/theme'
import { Link } from 'app/types'

import { Modal } from './BaseModal'

interface Props {
  open: boolean
  onClose: () => void
  link: Link
}

export const TransferModal: FC<Props> = ({ open, onClose, link }) => {
  const { namespace, shortpath, id } = link
  const transferToken = useGetTransferToken(id)
  const handleCopy = useClipboard(transferToken?.url)
  const fullShotPath = useFullShortPath({ namespace, shortpath })

  return (
    <Modal.Base open={open} onClose={onClose}>
      <Typography>
        To transfer ownership of <b>{fullShotPath}</b>, copy this link and send it to the new owner
      </Typography>
      <TextField
        value={transferToken?.url}
        sx={{
          borderRadius: '8px',
          p: 1,
          [media.TABLET]: {
            p: 2,
          },
        }}
        multiline
        disabled
      ></TextField>
      <Modal.Buttons>
        <Button variant='contained' onClick={handleCopy} disabled={!transferToken}>
          Copy
        </Button>
        <Button variant='contained' onClick={onClose}>
          Done
        </Button>
      </Modal.Buttons>
    </Modal.Base>
  )
}
