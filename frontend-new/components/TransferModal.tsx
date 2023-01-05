import { Typography } from '@mui/material'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import { FC, useCallback } from 'react'
import useSWR from 'swr'

import { Link } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

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
        <Typography>
          To transfer ownership of{' '}
          <b>
            {namespace}/{shortpath}
          </b>
          , copy this link and send it to the new owner
        </Typography>
      </div>
      <TextField
        value={transferToken?.url}
        sx={{
          borderRadius: '8px',
          p: 1,
          '@media (min-width: 840px)': {
            p: 2,
          },
        }}
        multiline
        disabled
      ></TextField>
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
