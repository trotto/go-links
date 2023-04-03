import { SvgIcon } from '@mui/material'
import { FC } from 'react'

import { media } from 'app/styles/theme'

export const Microsoft: FC = () => {
  return (
    <SvgIcon
      sx={{
        width: 24,
        height: 24,

        [media.TABLET]: {
          width: 28,
          height: 28,
        },

        [media.DESKTOP]: {
          width: 32,
          height: 32,
        },
      }}
      viewBox='0 0 33 32'
      fill='none'
      xmlns='http://www.w3.org/2000/svg'
    >
      <rect x='0.5' width='32' height='32' fill='url(#39b5cc1b-1f04-4432-b6bf-0eecb9459aa8)' />
      <defs>
        <pattern
          id='39b5cc1b-1f04-4432-b6bf-0eecb9459aa8'
          patternContentUnits='objectBoundingBox'
          width='1'
          height='1'
        >
          <use xlinkHref='#image0_576_1021' transform='scale(0.0104167)' />
        </pattern>
        <image
          id='image0_576_1021'
          width='96'
          height='96'
          xlinkHref='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA2xpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDAyIDc5LjE2NDM2MCwgMjAyMC8wMi8xMy0wMTowNzoyMiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo4RjhGQTUxRDUxMzAxMUU1QjVCMEQ0RTBBNDRBRDdENSIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpCRTBCQ0QyQTc5QTQxMUVEQTE5NEJBNTFGQ0NBMjU0QiIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpCRTBCQ0QyOTc5QTQxMUVEQTE5NEJBNTFGQ0NBMjU0QiIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxNSAoTWFjaW50b3NoKSI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOkNEODZDOEY2NzlBMzExRUQ4RDRDODg4RjUxMTkyMkU0IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOkNEODZDOEY3NzlBMzExRUQ4RDRDODg4RjUxMTkyMkU0Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+DT9GVgAAAOhJREFUeNrs3MENgkAQQNEdQwEklmIogC5shpNFedMGbMVQwsAeNfHoYfT9hJDMic0jsKeNdT5lq1eMt8fLYLqe+63cWg5NAAAIAAABACAAAAQAgAAAEAAAAgBAAAAIAAABACAAAAQAgAAAEAAAAgBAAAAIAAABACAAAAQAgABUadiv+KH1lFtLZKbX0CcIgAD86U/4eKn54M/lbXCvuZfou6CSR5Z9mDuyTAAACAAAAQAgAAAEAIAAABAAAAIAQAAACAAAAQAgAAAACAAAAQAgAAAEAIAAABAAAAIAQAAACAAAfa1NgAEA7UIOw/JF+tcAAAAASUVORK5CYII='
        />
      </defs>
    </SvgIcon>
  )
}
