import { SvgIcon } from '@mui/material'
import { FC } from 'react'

import { media } from 'app/styles/theme'

export const FailedCircle: FC = () => {
  return (
    <SvgIcon
      sx={{
        width: 16,
        height: 16,

        [media.TABLET]: {
          width: 24,
          height: 24,
        },

        [media.DESKTOP]: {
          width: 32,
          height: 32,
        },
      }}
      viewBox='0 0 32 32'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <circle cx='16' cy='16' r='16' fill='#C5443C' />
      <path
        d='M23.5 9L9.5 23'
        stroke='white'
        strokeWidth='2'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M9.5 9L23.5 23'
        stroke='white'
        strokeWidth='2'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
    </SvgIcon>
  )
}
