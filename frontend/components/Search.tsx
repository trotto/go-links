import { Box, InputAdornment, TextField } from '@mui/material'
import { ChangeEvent, FC, useCallback } from 'react'

import { Search as SearchIcon } from 'app/icons'
import { media } from 'app/styles/theme'

interface Props {
  value: string
  onChange: (value: string) => void
}

export const Search: FC<Props> = ({ value, onChange }) => {
  const handleChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => onChange(e.target.value),
    [onChange],
  )
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'space-around',
        alignItems: 'center',
        mt: 3,
        mb: 1,
        backgroundColor: '#f6f8fa',
        borderRadius: '32px',
        height: 32,
        [media.TABLET]: {
          mt: 5,
          mb: 2,
          height: 48,
        },
        [media.DESKTOP]: {
          mb: 3,
          height: 64,
        },
      }}
    >
      <TextField
        className='input'
        placeholder='Search keyword, domain or username'
        value={value}
        onChange={handleChange}
        sx={{
          backgroundColor: '#F6F8FA',
          p: 0,
          minWidth: 210,
          flexGrow: value ? 1 : 0,
          px: 2,
          '& input': {
            textAlign: 'center',
          },

          [media.TABLET]: {
            p: 0,
            minWidth: 250,
          },
          [media.DESKTOP]: {
            p: 0,
            minWidth: 290,
          },
        }}
        InputProps={{
          startAdornment: !value && (
            <InputAdornment position='start'>
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      ></TextField>
    </Box>
  )
}
