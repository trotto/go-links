import { FC, useCallback } from 'react'
import Button from '@mui/material/Button'
import { Link } from '../../../types'
import TextField from '@mui/material/TextField'
import useSWR from 'swr'
import { fetcher } from '../../../utils/fetcher'
import { Modal } from './BaseModal'

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
    <Modal.Base open={open} onClose={onClose}>
      <div>
        <p>
          To transfer ownership of{' '}
          <b>
            {namespace}/{shortpath}
          </b>
          , copy this link and send it to the new owner
        </p>
      </div>
      <TextField value={transferToken?.url} multiline disabled></TextField>
      <Modal.Buttons>
        <Button variant='contained' onClick={handleCopy}>
          Copy
        </Button>
        <Button variant='contained' onClick={onClose}>
          Done
        </Button>
      </Modal.Buttons>
    </Modal.Base>
  )
}
