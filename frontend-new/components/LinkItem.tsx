import styled from '@emotion/styled'
import { Box, Button, IconButton, TextField, Tooltip, Typography } from '@mui/material'
import { BoxProps } from '@mui/system'
import {
  ChangeEvent,
  FC,
  FormEvent,
  PropsWithChildren,
  useCallback,
  useState,
  useMemo,
} from 'react'

import { DeleteModal } from 'app/components/DeleteModal'
import { TransferModal } from 'app/components/TransferModal'
import { useUpdateLink, useDeleteLink, useModal, useClipboard } from 'app/hooks'
import { Copy, Edit } from 'app/icons'
import { Link } from 'app/types'

import { LinkActions } from './LinkActions'

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
      px: 1,
      height: 24,
      mr: 1,
      cursor: 'default',
      '@media (min-width: 840px)': {
        px: 2,
        mr: 3,
        height: 32,
      },
      ...sx,
    }}
  >
    <Typography variant={bold ? 'h3' : 'body1'}>{children}</Typography>
  </Box>
)

export const LinkItem: FC<Props> = ({ link, canEdit = false }) => {
  const { id, shortpath, destination_url, owner, namespace, visits_count } = link
  const [destination, setDestination] = useState(destination_url)
  const [editable, setEditable] = useState(false)

  const [transferModal, openTransferModal, closeTransferModal] = useModal()
  const [deleteModal, openDeleteModal, closeDeleteModal] = useModal()

  const fullShortPath = useMemo(
    () => `${namespace || window._trotto.defaultNamespace}/${shortpath}`,
    [namespace, shortpath],
  )
  const updateLink = useUpdateLink()
  const deleteLink = useDeleteLink()

  const handleDestinationChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => setDestination(e.target.value),
    [setDestination],
  )

  const handleCopy = useClipboard(fullShortPath)

  const handleEdit = useCallback(() => setEditable((editable) => !editable), [setEditable])

  const handleSave = useCallback(
    (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault()
      updateLink(id, { destination })
      handleEdit()
    },
    [destination, id, handleEdit, updateLink],
  )

  return (
    <>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 1,
          borderBottom: '1px solid #f0f0f0',
          backgroundColor: '#f6f8fa',
          // padding: '20px 8px',
          px: 1,
          py: 2.5,

          '@media (min-width: 840px)': {
            px: 3,
            py: 3.25,
            gap: 2,
          },

          '@media (min-width: 1440px)': {
            py: 3.75,
          },
        }}
      >
        <LabelRow>
          <InfoBox
            sx={{
              '@media (min-width: 840px)': {
                mr: 2,
              },
              fontWeight: 700,
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
            onTransfer={openTransferModal}
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
              mr: 1,
              '@media (min-width: 840px)': {
                mr: 3,
              },
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
                height: 24,
                flexGrow: 1,
                '@media (min-width: 840px)': {
                  height: 32,
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
                  height: 24,
                  '@media (min-width: 840px)': {
                    height: 32,
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
      </Box>
      {transferModal && (
        <TransferModal open={transferModal} onClose={closeTransferModal} link={link} />
      )}
      <DeleteModal
        open={deleteModal}
        onClose={closeDeleteModal}
        onDelete={deleteLink}
        link={link}
      />
    </>
  )
}
