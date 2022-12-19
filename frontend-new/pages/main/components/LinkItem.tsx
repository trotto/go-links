import { useState, useCallback, ChangeEvent, FormEvent } from 'react'
import { Link } from '../../../types'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import { LinkActions } from './LinkActions'
import styled from '@emotion/styled'
import { LinkUpdate } from '../../../types'
import { TransferModal } from '../modals/TransferModal'
import { DeleteModal } from '../modals/DeleteModal'
import { useSWRConfig } from 'swr'
import { fetcher } from '../../../utils/fetcher'

const StyledDiv = styled.div`
  border: 1px solid;
  padding: 10px;
  background-color: #d9d9d9;

  .button {
    margin: 10px;
  }

  .row {
    display: flex;

    .grow {
      flex-grow: 1;
    }
  }
`

interface Props {
  link: Link
}

export const LinkItem = ({ link }: Props) => {
  const { mutate } = useSWRConfig()
  const { id, shortpath, destination_url, owner, namespace, visits_count } = link
  const [destination, setDestination] = useState(destination_url)
  const [editable, setEditable] = useState(false)
  const [transferModal, setTransferModal] = useState(false)
  const [deleteModal, setDeleteModal] = useState(false)
  const fullShortPath = `${namespace || window._trotto.defaultNamespace}/${shortpath}`

  const handleDestinationChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => setDestination(e.target.value),
    [setDestination],
  )

  const handleCopy = useCallback(
    () => navigator.clipboard.writeText(fullShortPath),
    [fullShortPath],
  )

  const handleEdit = useCallback(() => setEditable((editable) => !editable), [setEditable])

  const openTrasferModal = useCallback(() => setTransferModal(true), [setTransferModal])
  const closeTrasferModal = useCallback(() => setTransferModal(false), [setTransferModal])
  const openDeleteModal = useCallback(() => setDeleteModal(true), [setDeleteModal])
  const closeDeleteModal = useCallback(() => setDeleteModal(false), [setDeleteModal])

  const handleDelete = useCallback(
    (id: number) =>
      fetcher<void>(`/_/api/links/${id}`, {
        method: 'DELETE',
      }).then(() => mutate('/_/api/links')),
    [mutate],
  )

  const handleUpdate = useCallback(
    (id: number, link: LinkUpdate) =>
      fetcher<Link>(`/_/api/links/${id}`, {
        method: 'PUT',
        body: JSON.stringify(link),
      }).then(() => mutate('/_/api/links')),
    [mutate],
  )

  const handleSave = useCallback(
    (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault()
      handleUpdate(id, { destination })
      handleEdit()
    },
    [destination, id, handleEdit],
  )

  return (
    <StyledDiv>
      <div className='row'>
        <TextField
          id='shorpath'
          className='grow'
          label='Keyword'
          variant='standard'
          value={fullShortPath}
          disabled
        />
        <Button className='button' variant='contained' onClick={handleCopy}>
          Copy
        </Button>
        <TextField id='owner' label='Owner' variant='standard' value={owner} disabled />
        <TextField id='visits' label='Visits' variant='standard' value={visits_count} disabled />
        <LinkActions onTransfer={openTrasferModal} onDelete={openDeleteModal} />
      </div>
      <form className='row' onSubmit={handleSave}>
        <TextField
          id='destination'
          className='grow'
          label='Keyword'
          variant='standard'
          value={destination}
          onChange={handleDestinationChange}
          disabled={!editable}
        />
        {editable && (
          <Button className='button' variant='contained' type='submit'>
            Save
          </Button>
        )}
        <Button className='button' variant='contained' onClick={handleEdit}>
          Edit
        </Button>
      </form>
      {transferModal && (
        <TransferModal open={transferModal} onClose={closeTrasferModal} link={link} />
      )}
      <DeleteModal
        open={deleteModal}
        onClose={closeDeleteModal}
        onDelete={handleDelete}
        link={link}
      />
    </StyledDiv>
  )
}
