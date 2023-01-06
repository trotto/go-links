import { FC, useCallback, useState, ChangeEvent } from 'react'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Modal from '@mui/material/Modal'
import { Link } from '../../../types'
import TextField from '@mui/material/TextField'

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
  onDelete: (id: number) => void
  onClose: () => void
  link: Link
}

export const DeleteModal: FC<Props> = ({ open, onClose, onDelete, link }) => {
  const { namespace, shortpath, id } = link
  const [confirmationPath, setConfirmationPath] = useState('')
  const fullShortPath = `${namespace || window._trotto.defaultNamespace}/${shortpath}`

  const handleConfirmationChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => setConfirmationPath(e.target.value),
    [setConfirmationPath],
  )

  const deleteLink = useCallback(() => {
    onDelete(id)
    onClose()
  }, [onDelete, onClose, id])

  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby='modal-modal-title'
      aria-describedby='modal-modal-description'
    >
      <Box sx={style}>
        <p>
          Deleting a go link will delete the go link for everyone in your organization. No one on
          your team will be able to use <b>{fullShortPath}</b> until it&#39s re-created.
        </p>
        <p>
          To confirm deletion, type <b>{fullShortPath}</b> and press Delete.
        </p>
        <TextField
          value={confirmationPath}
          label={fullShortPath}
          onChange={handleConfirmationChange}
        ></TextField>
        <div>
          <Button variant='contained' onClick={onClose}>
            Cancel
          </Button>
          <Button
            variant='contained'
            onClick={deleteLink}
            disabled={fullShortPath != confirmationPath}
          >
            Delete
          </Button>
        </div>
      </Box>
    </Modal>
  )
}
