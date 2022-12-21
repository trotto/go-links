import { useState, useCallback, ChangeEvent, FormEvent, useMemo } from 'react'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import { LinkCreate } from '../../../types'
import InputAdornment from '@mui/material/InputAdornment'
import styled from '@emotion/styled'
import EastRoundedIcon from '@mui/icons-material/EastRounded'

const StyledForm = styled.form`
  display: flex;

  .input {
    flex-grow: 1;
  }

  .circle-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 64px;
    height: 64px;
    background: #646ae7;
    border-radius: 32px;
    color: #fff;
    font-size: 16px;
    font-weight: 700;
  }

  .button {
    margin-left: 10px;
    height: 64px;

    font-weight: 700;
    padding: 0 32px;
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

  const isDisabled = useMemo(
    () => !formState.shortpath.length || !formState.destination.length,
    [formState],
  )

  return (
    <StyledForm onSubmit={handleSubmit}>
      <div className='circle-container'>{formState.namespace}/</div>
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
      <div className='circle-container'>
        <EastRoundedIcon />
      </div>
      <TextField
        id='destination'
        className='input'
        label='Paste the link to a resource here'
        variant='standard'
        value={formState.destination}
        onChange={handleChange}
      />
      <Button className='button' variant='contained' type='submit' disabled={isDisabled}>
        Create
      </Button>
    </StyledForm>
  )
}
