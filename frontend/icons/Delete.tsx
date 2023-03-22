import { SvgIcon } from '@mui/material'
import { FC } from 'react'

import { media } from 'app/styles/theme'

export const Delete: FC = () => {
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
      <path d='M2 4.5H3.33333H14' stroke='#343AAA' strokeLinecap='round' strokeLinejoin='round' />
      <path
        d='M5.33301 4.50001V3.16668C5.33301 2.81305 5.47348 2.47392 5.72353 2.22387C5.97358 1.97382 6.31272 1.83334 6.66634 1.83334H9.33301C9.68663 1.83334 10.0258 1.97382 10.2758 2.22387C10.5259 2.47392 10.6663 2.81305 10.6663 3.16668V4.50001M12.6663 4.50001V13.8333C12.6663 14.187 12.5259 14.5261 12.2758 14.7762C12.0258 15.0262 11.6866 15.1667 11.333 15.1667H4.66634C4.31272 15.1667 3.97358 15.0262 3.72353 14.7762C3.47348 14.5261 3.33301 14.187 3.33301 13.8333V4.50001H12.6663Z'
        stroke='#343AAA'
        strokeLinecap='round'
        strokeLinejoin='round'
      />
    </SvgIcon>
  )
}
