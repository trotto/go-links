import { SvgIcon } from '@mui/material'
import { FC } from 'react'

export const ArrowDown: FC = () => {
  return (
    <SvgIcon
      sx={{
        width: '24px',
        height: '12px',

        '@media (min-width: 840px)': {
          width: '32px',
          height: '16px',
        },

        '@media (min-width: 1440px)': {
          width: '40px',
          height: '20px',
        },
      }}
      width='40'
      height='20'
      viewBox='0 0 40 20'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path d='M40 0L20 20L0 0H40Z' fill='white' />
    </SvgIcon>
  )
}
