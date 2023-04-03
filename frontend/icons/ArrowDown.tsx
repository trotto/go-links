import { SvgIcon } from '@mui/material'
import { FC } from 'react'

import { media } from 'app/styles/theme'

export const ArrowDown: FC = () => {
  return (
    <SvgIcon
      sx={{
        width: 24,
        height: 12,

        [media.TABLET]: {
          width: 32,
          height: 16,
        },

        [media.DESKTOP]: {
          width: 40,
          height: 20,
        },
      }}
      viewBox='0 0 40 20'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <path d='M40 0L20 20L0 0H40Z' fill='white' />
    </SvgIcon>
  )
}
