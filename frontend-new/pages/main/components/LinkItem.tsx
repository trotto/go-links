import { useState, useCallback, ChangeEvent, FormEvent, PropsWithChildren, FC } from 'react'
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
import IconButton from '@mui/material/IconButton'
import Box from '@mui/material/Box'
import { BoxProps } from '@mui/system'
import { Copy, Edit } from '../../../icons'

const StyledDiv = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
  border-bottom: 1px solid #f0f0f0;
  padding: 24px 30px;
  background-color: #f6f8fa;

  .edit-group {
    display: flex;
    flex-grow: 1;
    flex-direction: row;
    border-radius: 32px;
    background: #fff;

    .button {
      background-color: #000;
    }
  }

  .row-1 {
    display: grid;
    grid-template-columns: max-content auto 1fr max-content 97px auto;
  }

  .grow {
    flex-grow: 1;
  }

  .row-2 {
    display: flex;

    .edit-group {
      display: flex;
      flex-direction: row;
      border-radius: 32px;
      background: #fff;
      margin-right: 16px;

      .button {
        background-color: #000;
      }
    }
  }
`

interface Props {
  link: Link
}

const InfoBox: FC<PropsWithChildren & { sx?: BoxProps['sx'] }> = ({ children, sx }) => (
  <Box
    sx={{
      backgroundColor: '#fff',
      borderRadius: '32px',
      display: 'flex',
      alignItems: 'center',
      px: '16px',
      ...sx,
    }}
  >
    {children}
  </Box>
)

export const LinkItem: FC<Props> = ({ link }) => {
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
    <>
      <StyledDiv>
        <div className='row-1'>
          <InfoBox
            sx={{
              fontSize: '16px',
              fontWeight: '700',
              mr: '8px',
            }}
          >
            {fullShortPath}
          </InfoBox>
          <IconButton onClick={handleCopy}>
            <Copy />
          </IconButton>
          <div></div>
          <InfoBox sx={{ mr: '24px' }}>{owner}</InfoBox>
          <InfoBox sx={{ mr: '16px' }}>{`${visits_count} visits`}</InfoBox>
          <LinkActions onTransfer={openTrasferModal} onDelete={openDeleteModal} />
        </div>
        <form className='row-2' onSubmit={handleSave}>
          <div className='edit-group grow'>
            <TextField
              id='destination'
              className='grow'
              placeholder='Keyword'
              value={destination}
              onChange={handleDestinationChange}
              disabled={!editable}
            />
            {editable && (
              <Button className='button' variant='contained' type='submit'>
                Save
              </Button>
            )}
          </div>
          <IconButton onClick={handleEdit}>
            <Edit />
          </IconButton>
        </form>
      </StyledDiv>
      {transferModal && (
        <TransferModal open={transferModal} onClose={closeTrasferModal} link={link} />
      )}
      <DeleteModal
        open={deleteModal}
        onClose={closeDeleteModal}
        onDelete={handleDelete}
        link={link}
      />
    </>
  )
}
