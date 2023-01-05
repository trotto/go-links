import { SvgIcon } from '@mui/material'
import { FC } from 'react'

export const FailedCircle: FC = () => {
  return (
    <SvgIcon
      sx={{
        width: '16px',
        height: '16px',

        '@media (min-width: 840px)': {
          width: '24px',
          height: '24px',
        },

        '@media (min-width: 1440px)': {
          width: '32px',
          height: '32px',
        },
      }}
      width='32'
      height='32'
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
