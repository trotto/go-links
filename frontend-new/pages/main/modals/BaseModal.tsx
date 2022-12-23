import { FC, PropsWithChildren } from 'react'
import { Box, Modal as MuiModal } from '@mui/material'
import styled from '@emotion/styled'

const style = {
  position: 'absolute',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  gap: '16px',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 648,
  bgcolor: 'background.paper',
  boxShadow: 24,
  padding: '40px 64px',
  color: '#343aaa',
  background: '#F4F3FF',
  borderRadius: '8px',
}

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
        <Box sx={style}>{children}</Box>
      </MuiModal>
    </Container>
  )
}

export const Modal = {
  Buttons,
  Base,
}
