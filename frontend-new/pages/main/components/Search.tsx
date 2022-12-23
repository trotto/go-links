import { FC, useCallback, ChangeEvent } from 'react'
import { TextField, InputAdornment } from '@mui/material'
import SearchRoundedIcon from '@mui/icons-material/SearchRounded'
import styled from '@emotion/styled'

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 40px 0 24px;
  background-color: #f6f8fa;
  height: 64px;
  border-radius: 32px;
`

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
    <Container>
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
    </Container>
  )
}
