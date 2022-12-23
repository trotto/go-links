import styled from '@emotion/styled'
import EastRoundedIcon from '@mui/icons-material/EastRounded'
import { Button, TextField } from '@mui/material'
import { ChangeEvent, FormEvent, useCallback, useMemo, useState } from 'react'

import { LinkCreate } from 'app/types'

const StyledForm = styled.form`
  display: grid;
  grid-template-columns: 5fr 8fr;
  gap: 8px;
`

const Group = styled.div`
  display: flex;
  flex-direction: row;
  background-color: #f4f3ff;
  border-radius: 32px;
`

const Cicle = styled.div`
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
      <Group>
        <Cicle>{formState.namespace}/</Cicle>
        <TextField
          id='shortpath'
          placeholder='Keyword'
          value={formState.shortpath}
          onChange={handleChange}
          sx={{
            flexGrow: 1,
            backgroundColor: '#f4f3ff',
            '& input, & input::placeholder': {
              color: '#343AAA',
              opacity: 1,
            },
          }}
        />
      </Group>

      <Group className='group'>
        <Cicle>
          <EastRoundedIcon />
        </Cicle>
        <TextField
          id='destination'
          placeholder='Paste the link to a resource here'
          value={formState.destination}
          onChange={handleChange}
          sx={{
            flexGrow: 1,
            backgroundColor: '#f4f3ff',
            '& input, & input::placeholder': {
              color: '#343AAA',
              opacity: 1,
            },
          }}
        />
        <Button
          variant='contained'
          type='submit'
          disabled={isDisabled}
          sx={{
            height: '64px',
            fontWeight: '700',
            px: '32px',
          }}
        >
          Create
        </Button>
      </Group>
    </StyledForm>
  )
}
