import { Box, BoxProps, IconButton } from '@mui/material'
import { FC } from 'react'

import { DeleteModal } from 'app/components/DeleteModal'
import { TransferModal } from 'app/components/TransferModal'
import { useModal, useClipboard, useFullShortPath } from 'app/hooks'
import { Copy, Eye } from 'app/icons'
import { media } from 'app/styles/theme'
import { Link } from 'app/types'

import { EditableDestination } from './EditableDestination'
import { InfoBox } from './InfoBox'
import { LinkActions } from './LinkActions'

interface Props {
  link: Link
  canEdit?: boolean
  sx?: BoxProps['sx']
}

export const LinkItem: FC<Props> = ({ link, canEdit = false, sx }) => {
  const { id, destination_url, owner, visits_count } = link
  const fullShortPath = useFullShortPath(link)

  const [transferModal, openTransferModal, closeTransferModal] = useModal()
  const [deleteModal, openDeleteModal, closeDeleteModal] = useModal()

  const handleCopy = useClipboard(fullShortPath)

  return (
    <>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 1,
          borderBottom: '1px solid #f0f0f0',
          px: 1,
          py: 2.5,

          [media.TABLET]: {
            px: 3,
            py: 3.25,
            gap: 2,
          },

          [media.DESKTOP]: {
            py: 3.75,
          },
          ...sx,
        }}
      >
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: 'max-content auto 1fr minmax(68px, max-content) max-content auto',
            alignItems: 'center',
          }}
        >
          <InfoBox
            sx={{
              [media.TABLET]: {
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
          <InfoBox sx={{ ml: 1 }}>{owner}</InfoBox>
          <InfoBox>
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                [media.TABLET]: {
                  display: 'inline',
                },
              }}
            >
              {visits_count}{' '}
              <Box
                sx={{
                  display: 'none',
                  [media.TABLET]: {
                    display: 'inline',
                  },
                }}
              >
                {' '}
                visits
              </Box>
              <Box
                sx={{
                  display: 'flex',
                  ml: 1,
                  [media.TABLET]: {
                    display: 'none',
                  },
                }}
              >
                <Eye />
              </Box>
            </Box>
          </InfoBox>
          <LinkActions
            disabled={!canEdit}
            onTransfer={openTransferModal}
            onDelete={openDeleteModal}
          />
        </Box>
        <EditableDestination id={id} destinationUrl={destination_url} disabled={!canEdit} />
      </Box>
      {transferModal && (
        <TransferModal open={transferModal} onClose={closeTransferModal} link={link} />
      )}
      <DeleteModal open={deleteModal} onClose={closeDeleteModal} link={link} />
    </>
  )
}
