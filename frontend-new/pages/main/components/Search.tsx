import SearchRoundedIcon from '@mui/icons-material/SearchRounded'
import { Box, InputAdornment, TextField } from '@mui/material'
import { ChangeEvent, FC, useCallback } from 'react'

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
        justifyContent: 'center',
        alignItems: 'center',
        mt: '24px',
        mb: '8px',
        backgroundColor: '#f6f8fa',
        borderRadius: '32px',
        height: '32px',
        '@media (min-width: 839px)': {
          mt: '40px',
          mb: '16px',
          height: '48px',
        },
        '@media (min-width: 1032px)': {
          mb: '24px',
          height: '64px',
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
          width: '291px',
          padding: 0,
        }}
        InputProps={{
          startAdornment: (
            <InputAdornment position='start'>
              <SearchRoundedIcon sx={{ width: '16px', height: '16px', color: '#000' }} />
            </InputAdornment>
          ),
        }}
      ></TextField>
    </Box>
  )
}
