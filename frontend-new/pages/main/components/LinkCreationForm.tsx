import { useState, useCallback, ChangeEvent, FormEvent } from 'react'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import { LinkCreate } from '../../../types'
import InputAdornment from '@mui/material/InputAdornment'
import styled from '@emotion/styled'

const StyledForm = styled.form`
  display: flex;

  .input {
    flex-grow: 1;
  }

  .button {
    margin: 10px;
  }
`

interface Props {
  onCreate: (link: LinkCreate) => void
}

export const LinkCreationForm = ({ onCreate }: Props) => {
  const [formState, setFormState] = useState<LinkCreate>({
    shortpath: '',
    destination: '',
    namespace: 'go',
  })

  const handleChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) =>
      setFormState((formState) => ({ ...formState, [e.target.id]: e.target.value })),
    [],
  )

  const handleSubmit = useCallback(
    (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault()
      onCreate(formState)
    },
    [formState],
  )

  return (
    <StyledForm onSubmit={handleSubmit}>
      <TextField
        id='shortpath'
        className='input'
        label='Keyword'
        variant='standard'
        value={formState.shortpath}
        onChange={handleChange}
        InputProps={{
          startAdornment: (
            <InputAdornment position='start' sx={{ marginRight: 0 }}>
              {formState.namespace}/
            </InputAdornment>
          ),
        }}
      />
      <b> &#8594; </b>
      <TextField
        id='destination'
        className='input'
        label='Paste the link to a resource here'
        variant='standard'
        value={formState.destination}
        onChange={handleChange}
      />
      <Button className='button' variant='contained' type='submit'>
        Create
      </Button>
    </StyledForm>
  )
}
