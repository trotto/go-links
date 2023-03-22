import { SvgIcon } from '@mui/material'
import { FC } from 'react'

import { media } from 'app/styles/theme'

export const Search: FC = () => {
  return (
    <SvgIcon
      sx={{
        color: '#000',
        width: 10,
        height: 10,

        [media.TABLET]: {
          width: 12,
          height: 12,
        },

        [media.DESKTOP]: {
          width: 14,
          height: 14,
        },
      }}
      viewBox='0 0 14 14'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path
        d='M5.89645 9.80634C8.32826 9.80634 10.2996 7.83497 10.2996 5.40317C10.2996 2.97137 8.32826 1 5.89645 1C3.46465 1 1.49329 2.97137 1.49329 5.40317C1.49329 7.83497 3.46465 9.80634 5.89645 9.80634Z'
        stroke='black'
        strokeWidth='1.2'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
      <path
        d='M9.37366 8.97729L13.1633 12.9012'
        stroke='black'
        strokeWidth='1.2'
        strokeLinecap='round'
      />
    </SvgIcon>
  )
}
