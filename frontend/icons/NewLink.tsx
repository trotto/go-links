import { SvgIcon } from '@mui/material'
import { FC } from 'react'

import { media } from 'app/styles/theme'

export const NewLink: FC = () => {
  return (
    <SvgIcon
      sx={{
        width: 81,
        height: 48,
        transform: 'translateX(-13px)',

        [media.TABLET]: {
          width: 102,
          height: 72,
          transform: 'translateX(-18px)',
        },

        [media.DESKTOP]: {
          width: 136,
          height: 88,
          transform: 'translateX(-24px)',
        },
      }}
      viewBox='0 0 136 88'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <rect x='8' y='30' width='32' height='4' fill='white' />
      <rect y='42' width='32' height='4' fill='white' />
      <rect x='8' y='54' width='32' height='4' fill='white' />
      <circle cx='92' cy='44' r='44' fill='white' />
      <rect
        x='66'
        y='24'
        width='52.8'
        height='40'
        fill='url(#5c318dce-beb9-4a91-8592-5646a21e2c6f)'
      />
      <defs>
        <pattern
          id='5c318dce-beb9-4a91-8592-5646a21e2c6f'
          patternContentUnits='objectBoundingBox'
          width='1'
          height='1'
        >
          <use
            xlinkHref='#image0_464_7203'
            transform='translate(0 -0.00159999) scale(0.01 0.0132)'
          />
        </pattern>
        <image
          id='image0_464_7203'
          width='100'
          height='76'
          xlinkHref='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABMCAYAAACbHRIPAAAACXBIWXMAAAsTAAALEwEAmpwYAAAGTGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNi4wLWMwMDIgNzkuMTY0MzYwLCAyMDIwLzAyLzEzLTAxOjA3OjIyICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIyLTEyLTE0VDE1OjM5OjI2LTAzOjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDIyLTEyLTE0VDE1OjM5OjI2LTAzOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMi0xMi0xNFQxNTozOToyNi0wMzowMCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpjNDg2MzNkNS05YWI5LWZkNGItYjU3OS05YjRlNTVhMzgxOGUiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDpkYmIzOWZiMy1mMDhhLTAzNDAtOTM3Zi1mYjVjMDQyMWM1Y2IiIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDoyOWRmZDQ2Ny01NmNiLTU0NGMtYjQ3Yy0yNGUzNzhiZjQ2N2EiIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIj4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDoyOWRmZDQ2Ny01NmNiLTU0NGMtYjQ3Yy0yNGUzNzhiZjQ2N2EiIHN0RXZ0OndoZW49IjIwMjItMTItMTRUMTU6Mzk6MjYtMDM6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMS4xIChXaW5kb3dzKSIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6YzQ4NjMzZDUtOWFiOS1mZDRiLWI1NzktOWI0ZTU1YTM4MThlIiBzdEV2dDp3aGVuPSIyMDIyLTEyLTE0VDE1OjM5OjI2LTAzOjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjEuMSAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDxwaG90b3Nob3A6RG9jdW1lbnRBbmNlc3RvcnM+IDxyZGY6QmFnPiA8cmRmOmxpPjgyMjg1MjI3RUUyQTc3NzUxODYwRjUyNzdFODk5OTdGPC9yZGY6bGk+IDwvcmRmOkJhZz4gPC9waG90b3Nob3A6RG9jdW1lbnRBbmNlc3RvcnM+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+5WKMhgAACpdJREFUeJzt3HuQVnUZwPHPLisJWq6EOnhBU3FQMQHxLo6WTVqG4SVNSgqtpnQ0pbQm0iwtrUzGrCwvWSZFKZaVWuMtm7hIiaYgopg63lIEDJVAYPvj2ddd6X3P7b3su4vfmR2W9/zO+f32fc55fs/1tHR0dHiL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'
        />
      </defs>
    </SvgIcon>
  )
}
