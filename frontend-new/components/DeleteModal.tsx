import { Button, TextField, Typography } from '@mui/material'
import { ChangeEvent, FC, useCallback, useState } from 'react'

import { useDeleteLink, useFullShortPath } from 'app/hooks'
import { Link } from 'app/types'

import { Modal } from './BaseModal'

interface Props {
  open: boolean
  onClose: () => void
  link: Link
}

export const DeleteModal: FC<Props> = ({ open, onClose, link }) => {
  const { id } = link
  const [confirmationPath, setConfirmationPath] = useState('')
  const fullShortPath = useFullShortPath(link)
  const deleteLink = useDeleteLink()

  const handleConfirmationChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => setConfirmationPath(e.target.value),
    [setConfirmationPath],
  )

  const handleDelete = useCallback(() => {
    deleteLink(id)
    onClose()
  }, [deleteLink, onClose, id])

  return (
    <Modal.Base open={open} onClose={onClose}>
      <Typography>
        Deleting a go link will delete the go link for everyone in your organization. No one on your
        team will be able to use <b>{fullShortPath}</b> until it&apos;s re-created.
      </Typography>
      <Typography>
        To confirm deletion, type <b>{fullShortPath}</b> and press Delete.
      </Typography>
      <TextField
        value={confirmationPath}
        placeholder={fullShortPath}
        onChange={handleConfirmationChange}
      ></TextField>
      <Modal.Buttons>
        <Button variant='contained' onClick={onClose}>
          Cancel
        </Button>
        <Button
          variant='contained'
          onClick={handleDelete}
          disabled={fullShortPath != confirmationPath}
        >
          Delete
        </Button>
      </Modal.Buttons>
    </Modal.Base>
  )
}
