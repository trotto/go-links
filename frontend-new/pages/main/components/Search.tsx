import { FC, useCallback, ChangeEvent } from 'react'
import TextField from '@mui/material/TextField'
import styled from '@emotion/styled'
import InputAdornment from '@mui/material/InputAdornment'
import SearchRoundedIcon from '@mui/icons-material/SearchRounded'

const StyledDiv = styled.div`
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
    <StyledDiv>
      <div className='input-container'>
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
      </div>
    </StyledDiv>
  )
}
