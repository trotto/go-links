import { Box, Typography } from '@mui/material'
import { FC } from 'react'

import { FailedCircle, SuccessCircle } from 'app/icons'
import { media } from 'app/styles/theme'
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
    <Box sx={{ mt: 3, backgroundColor: type === ResponseType.SUCCESS ? '#EFF6FF' : '#f6f8fa' }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'row',
          justifyContent: 'center',
          alignItems: 'center',
          border: '1px solid #dedede',
          lineHeight: '24px',
          backgroundColor: type === ResponseType.SUCCESS ? '#2885FF' : '#fff',
          color: type === ResponseType.SUCCESS ? '#fff' : '#000',
          gap: 1,

          height: 48,

          [media.TABLET]: {
            gap: 2,
            height: 72,
          },
          [media.DESKTOP]: {
            gap: 3,
            height: 80,
          },
        }}
      >
        {type === ResponseType.SUCCESS ? <SuccessCircle /> : <FailedCircle />}
        <Typography variant='h2' sx={{ fontWeight: '700' }}>
          {message}
        </Typography>
      </Box>
      <LinkItem
        link={link}
        sx={
          type === ResponseType.SUCCESS
            ? {
                '& .MuiButton-root': {
                  backgroundColor: '#2885FF',
                  '&:hover': { backgroundColor: '#0148A6' },
                },
              }
            : {}
        }
      ></LinkItem>
    </Box>
  )
}
