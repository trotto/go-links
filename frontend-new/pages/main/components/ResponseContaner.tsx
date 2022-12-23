import { Box } from '@mui/material'

import { FailedCircle, SuccessCircle } from 'app/icons'
import { Link } from 'app/types'

import { LinkItem } from './LinkItem'

export enum ResponseType {
  SUCCESS = 'success',
  ERROR = 'error',
}

interface Props {
  link: Link
  type: ResponseType
  message: string
}

export const ResponseContainer = ({ link, message, type }: Props) => {
  return (
    <Box sx={{ mt: '24px' }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'row',
          justifyContent: 'center',
          alignItems: 'center',
          height: '80px',
          border: '1px solid #dedede',
          fontWeight: '700',
          fontSize: '16px',
          lineHeight: '24px',
          backgroundColor: type === ResponseType.SUCCESS ? '#2885FF' : '#fff',
          color: type === ResponseType.SUCCESS ? '#fff' : '#000',
          gap: '24px',
        }}
      >
        {type === ResponseType.SUCCESS ? <SuccessCircle /> : <FailedCircle />}
        <p>{message}</p>
      </Box>
      <LinkItem link={link}></LinkItem>
    </Box>
  )
}
