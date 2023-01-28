import styled from '@emotion/styled'
import { Box, Modal as MuiModal } from '@mui/material'
import { FC, PropsWithChildren } from 'react'

import { media } from 'app/styles/theme'

const Buttons = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
`

const Container = styled.div`
  .MuiBackdrop-root {
    background-color: red;
  }
`

interface Props extends PropsWithChildren {
  open: boolean
  onClose: () => void
}

const Base: FC<Props> = ({ open, onClose, children }) => {
  return (
    <Container>
      <MuiModal
        open={open}
        onClose={onClose}
        aria-labelledby='modal-modal-title'
        aria-describedby='modal-modal-description'
        slotProps={{ backdrop: { style: { backgroundColor: '#131878', opacity: 0.6 } } }}
      >
        <Box
          sx={{
            position: 'absolute',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            gap: 1,
            top: '50%',
            transform: 'translateY(-50%)',
            left: 16,
            right: 16,
            p: 3,
            bgcolor: 'background.paper',
            boxShadow: 24,
            color: '#343aaa',
            background: '#F4F3FF',
            borderRadius: '8px',

            [media.TABLET]: {
              left: '50%',
              transform: 'translate(-50%, -50%)',
              gap: 2,
              px: 7,
              py: 4,
              width: 596,
            },
            [media.DESKTOP]: {
              width: 648,
              py: 5,
              px: 8,
            },
          }}
        >
          {children}
        </Box>
      </MuiModal>
    </Container>
  )
}

export const Modal = {
  Buttons,
  Base,
}
