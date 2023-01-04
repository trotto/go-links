import styled from '@emotion/styled'
import { Box, Modal as MuiModal } from '@mui/material'
import { FC, PropsWithChildren } from 'react'

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
            gap: '8px',
            top: '50%',
            transform: 'translateY(-50%)',
            left: '16px',
            right: '16px',
            padding: '24px 24px',

            '@media (min-width: 839px)': {
              left: '50%',
              transform: 'translate(-50%, -50%)',
              gap: '16px',
              padding: '32px 56px',
              width: '596px',
            },
            '@media (min-width: 1032px)': {
              width: '648px',
              padding: '40px 64px',
            },
            bgcolor: 'background.paper',
            boxShadow: 24,
            color: '#343aaa',
            background: '#F4F3FF',
            borderRadius: '8px',
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
