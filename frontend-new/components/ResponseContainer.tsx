import { Box, Typography } from '@mui/material'
import { FC } from 'react'

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

export const ResponseContainer: FC<Props> = ({ link, message, type }) => {
  return (
    <Box sx={{ mt: 3 }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'row',
          justifyContent: 'center',
          alignItems: 'center',
          height: 80,
          border: '1px solid #dedede',
          lineHeight: '24px',
          backgroundColor: type === ResponseType.SUCCESS ? '#2885FF' : '#fff',
          color: type === ResponseType.SUCCESS ? '#fff' : '#000',
          gap: 3,
        }}
      >
        {type === ResponseType.SUCCESS ? <SuccessCircle /> : <FailedCircle />}
        <Typography variant='h2' sx={{ fontWeight: '700' }}>
          {message}
        </Typography>
      </Box>
      <LinkItem link={link}></LinkItem>
    </Box>
  )
}
