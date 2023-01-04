import styled from '@emotion/styled'
import { Box, Button, IconButton, TextField, Tooltip, Typography } from '@mui/material'
import { BoxProps } from '@mui/system'
import { ChangeEvent, FC, FormEvent, PropsWithChildren, useCallback, useState } from 'react'
import { useSWRConfig } from 'swr'

import { Copy, Edit } from 'app/icons'
import { DeleteModal } from 'app/pages/main/modals/DeleteModal'
import { TransferModal } from 'app/pages/main/modals/TransferModal'
import { Link, LinkUpdate } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

import { LinkActions } from './LinkActions'

const Container = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-bottom: 1px solid #f0f0f0;
  background-color: #f6f8fa;
  padding: 20px 8px;

  @media (min-width: 839px) {
    padding: 26px 24px;
    gap: 16px;
  }

  @media (min-width: 1032px) {
    padding: 30px 24px;
  }
`

const LabelRow = styled.div`
  display: grid;
  grid-template-columns: max-content auto 1fr max-content max-content auto;
  align-items: center;
`

const Form = styled.form`
  display: flex;
  align-items: center;
`

interface Props {
  link: Link
  canEdit?: boolean
}

const InfoBox: FC<PropsWithChildren & { sx?: BoxProps['sx']; bold?: boolean }> = ({
  children,
  sx,
  bold = false,
}) => (
  <Box
    sx={{
      backgroundColor: '#fff',
      borderRadius: '32px',
      display: 'flex',
      alignItems: 'center',
      px: '8px',
      height: '24px',
      mr: '24px',
      cursor: 'default',
      '@media (min-width: 839px)': {
        px: '16px',
        height: '32px',
      },
      ...sx,
    }}
  >
    <Typography variant={bold ? 'h3' : 'body1'}>{children}</Typography>
  </Box>
)

export const LinkItem: FC<Props> = ({ link, canEdit = false }) => {
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
      <Container>
        <LabelRow>
          <InfoBox
            sx={{
              mr: '16px',
              fontWeight: '700',
            }}
            bold
          >
            {fullShortPath}
          </InfoBox>
          <IconButton
            onClick={handleCopy}
            sx={{
              opacity: 0.25,
              '&:focus': {
                opacity: 1,
              },
            }}
          >
            <Copy />
          </IconButton>
          <div />
          <InfoBox>{owner}</InfoBox>
          <InfoBox>{`${visits_count} visits`}</InfoBox>
          <LinkActions
            disabled={!canEdit}
            onTransfer={openTrasferModal}
            onDelete={openDeleteModal}
          />
        </LabelRow>
        <Form onSubmit={handleSave}>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'row',
              borderRadius: '32px',
              background: '#fff',
              mr: '24px',
              flexGrow: 1,
            }}
          >
            <TextField
              id='destination'
              placeholder='Keyword'
              value={destination}
              onChange={handleDestinationChange}
              disabled={!editable}
              sx={{
                height: '24px',
                flexGrow: 1,
                '@media (min-width: 839px)': {
                  height: '32px',
                },
              }}
            />
            {editable && (
              <Button
                className='button'
                variant='contained'
                type='submit'
                sx={{
                  backgroundColor: '#000',
                  height: '24px',
                  '@media (min-width: 839px)': {
                    height: '32px',
                  },
                }}
              >
                Save
              </Button>
            )}
          </Box>
          <Tooltip title={!canEdit && 'You don’t have permission to modify this go link'}>
            <span>
              <IconButton
                onClick={handleEdit}
                sx={{
                  opacity: editable ? 1 : 0.25,
                  '&:disabled': {
                    opacity: 0.1,
                  },
                }}
                disabled={!canEdit}
              >
                <Edit />
              </IconButton>
            </span>
          </Tooltip>
        </Form>
      </Container>
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
