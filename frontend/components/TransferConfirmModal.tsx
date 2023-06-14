import { Typography } from '@mui/material'
import Button from '@mui/material/Button'
import { FC, useCallback } from 'react'

import { useFullShortPath, useTransferConfirm } from 'app/hooks'
import { Link } from 'app/types'

import { Modal } from './BaseModal'

interface Props {
  open: boolean
  onClose: () => void
  link: Link
  transferToken: string
}

export const TransferConfirmModal: FC<Props> = ({ open, onClose, link, transferToken }) => {
  const { namespace, shortpath } = link
  const fullShortPath = useFullShortPath({ namespace, shortpath })
  const confirmTransfer = useTransferConfirm(transferToken, fullShortPath)

  const onConfirm = useCallback(() => {
    confirmTransfer()
    onClose()
  }, [confirmTransfer, onClose])

  return (
    <Modal.Base open={open} onClose={onClose} fitContent>
      <Typography>
        Would you like to take ownership of <b>{fullShortPath}</b>?
      </Typography>
      <Modal.Buttons>
        <Button variant='contained' onClick={onClose}>
          Cancel
        </Button>
        <Button variant='contained' onClick={onConfirm}>
          Take ownership
        </Button>
      </Modal.Buttons>
    </Modal.Base>
  )
}
