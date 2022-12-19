import { FC, useCallback, ChangeEvent } from 'react'
import TextField from '@mui/material/TextField'
import styled from '@emotion/styled'

const StyledDiv = styled.div`
  display: flex;
  background-color: #fff;
  margin: 40px 0 24px;

  .input {
    flex-grow: 1;
  }
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
      <TextField
        className='input'
        label='Search keyword, domain or username'
        value={value}
        onChange={handleChange}
      ></TextField>
    </StyledDiv>
  )
}
