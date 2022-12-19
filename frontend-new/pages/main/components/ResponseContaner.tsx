import { useState, useCallback, ChangeEvent, FormEvent } from 'react'
import { Link } from '../../../types'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import { LinkActions } from './LinkActions'
import styled from '@emotion/styled'
import { LinkUpdate } from '../../../types'
import { TransferModal } from '../modals/TransferModal'
import { DeleteModal } from '../modals/DeleteModal'
import { LinkItem } from './LinkItem'

const StyledDiv = styled.div(({ type }: { type: ResponseType }) => ({
  border: '1px solid',
  borderRadius: '4px',
  '.header': {
    display: 'flex',
    justifyContent: 'center',
    padding: '26px',
    backgroundColor: '#fff',
    fontSize: '20px',
    fontWeight: 600,
  },
}))

export enum ResponseType {
  SUCCESS = 'success',
  ERROR = 'error',
}

interface Props {
  link: Link
  type: ResponseType
  message: string
}

export const ResponseContainer = ({ link, type, message }: Props) => {
  return (
    <StyledDiv type={type}>
      <div className='header'>{message}</div>
      <LinkItem link={link}></LinkItem>
    </StyledDiv>
  )
}
