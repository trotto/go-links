import SearchRoundedIcon from '@mui/icons-material/SearchRounded'
import { Box, InputAdornment, TextField } from '@mui/material'
import { ChangeEvent, FC, useCallback } from 'react'

import { Search as SearchIcon } from 'app/icons'

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
        '@media (min-width: 840px)': {
          mt: 5,
          mb: 2,
          height: 48,
        },
        '@media (min-width: 1440px)': {
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
          width: 210,
          '@media (min-width: 840px)': {
            p: 0,
            width: 250,
          },
          '@media (min-width: 1440px)': {
            p: 0,
            width: 290,
          },
        }}
        InputProps={{
          startAdornment: (
            <InputAdornment position='start'>
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      ></TextField>
    </Box>
  )
}
