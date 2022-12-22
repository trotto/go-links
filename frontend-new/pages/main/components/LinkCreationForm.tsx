import { useState, useCallback, ChangeEvent, FormEvent, useMemo } from 'react'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import { LinkCreate } from '../../../types'
import styled from '@emotion/styled'
import EastRoundedIcon from '@mui/icons-material/EastRounded'

const StyledForm = styled.form`
  display: grid;
  grid-template-columns: 5fr 8fr;
  gap: 8px;

  .input {
    flex-grow: 1;
  }

  .group {
    display: flex;
    flex-direction: row;
    background-color: #f4f3ff;
    border-radius: 32px;
  }

  .circle-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 64px;
    height: 64px;
    background-color: #646ae7;
    border-radius: 32px;
    color: #fff;
    font-size: 16px;
    font-weight: 700;
  }

  .button {
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
      <div className='group'>
        <div className='circle-container'>{formState.namespace}/</div>
        <TextField
          id='shortpath'
          className='input'
          placeholder='Keyword'
          value={formState.shortpath}
          onChange={handleChange}
          sx={{
            backgroundColor: '#f4f3ff',
            '& input, & input::placeholder': {
              color: '#343AAA',
              opacity: 1,
            },
          }}
        />
      </div>

      <div className='group'>
        <div className='circle-container'>
          <EastRoundedIcon />
        </div>
        <TextField
          id='destination'
          className='input'
          placeholder='Paste the link to a resource here'
          value={formState.destination}
          onChange={handleChange}
          sx={{
            backgroundColor: '#f4f3ff',
            '& input, & input::placeholder': {
              color: '#343AAA',
              opacity: 1,
            },
          }}
        />
        <Button className='button' variant='contained' type='submit' disabled={isDisabled}>
          Create
        </Button>
      </div>
    </StyledForm>
  )
}
