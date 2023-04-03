import { SvgIcon } from '@mui/material'
import { FC } from 'react'

import { media } from 'app/styles/theme'

export const Transfer: FC = () => {
  return (
    <SvgIcon
      sx={{
        width: 12,
        height: 12,

        [media.TABLET]: {
          height: 16,
          width: 16,
        },
      }}
      viewBox='0 0 16 17'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <g clipPath='url(#clip0_576_9210)'>
        <path
          d='M4.66667 15.8333L2 13.1667L4.66667 10.5'
          stroke='#343AAA'
          strokeLinecap='round'
          strokeLinejoin='round'
        />
        <path
          d='M14 9.16666V10.5C14 11.2072 13.719 11.8855 13.219 12.3856C12.7189 12.8857 12.0406 13.1667 11.3333 13.1667H2'
          stroke='#343AAA'
          strokeLinecap='round'
          strokeLinejoin='round'
        />
        <path
          d='M11.333 1.16666L13.9997 3.83332L11.333 6.49999'
          stroke='#343AAA'
          strokeLinecap='round'
          strokeLinejoin='round'
        />
        <path
          d='M2 7.83334V6.50001C2 5.79277 2.28095 5.11449 2.78105 4.61439C3.28115 4.11429 3.95942 3.83334 4.66667 3.83334H14'
          stroke='#343AAA'
          strokeLinecap='round'
          strokeLinejoin='round'
        />
      </g>
      <defs>
        <clipPath id='clip0_576_9210'>
          <rect width='16' height='16' fill='white' transform='translate(0 0.5)' />
        </clipPath>
      </defs>
    </SvgIcon>
  )
}
