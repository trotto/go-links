import styled from '@emotion/styled'
import EastRoundedIcon from '@mui/icons-material/EastRounded'
import { Button, TextField, Typography, Box, useMediaQuery } from '@mui/material'
import { useRouter } from 'next/router'
import { ChangeEvent, FormEvent, useCallback, useMemo, useState } from 'react'
import { useEffect, useRef, FC } from 'react'

import { useSaveLink } from 'app/hooks'
import { media } from 'app/styles/theme'
import { LinkCreate, LinkCreateResponse } from 'app/types'

const Group = styled.div`
  display: flex;
  flex-direction: row;
  background-color: #f4f3ff;
  border-radius: 32px;
`

const Circle = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 32px;
  height: 32px;
  background-color: #bdbcf3;
  border-radius: 32px 0px 0px 32px;
  color: #fff;

  ${media.TABLET} {
    width: 48px;
    height: 48px;
  }

  ${media.DESKTOP} {
    width: 64px;
    height: 64px;
  }
`

interface Props {
  onCreate: ({
    link,
    createdResponse,
  }: {
    link: LinkCreate
    createdResponse: LinkCreateResponse
  }) => void
}

export const LinkCreationForm: FC<Props> = ({ onCreate }) => {
  const {
    query: { sp },
  } = useRouter()
  const [formState, setFormState] = useState<LinkCreate>({
    shortpath: '',
    destination: '',
    namespace: 'go',
  })
  const saveLink = useSaveLink()

  const shortInpuRef = useRef<HTMLInputElement>(null)
  const destInpuRef = useRef<HTMLInputElement>(null)
  const isTablet = useMediaQuery(media.TABLET)

  const handleChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) =>
      setFormState((formState) => ({ ...formState, [e.target.id]: e.target.value })),
    [],
  )

  const handleSubmit = useCallback(
    async (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault()
      const createdResponse = await saveLink(formState)
      if (createdResponse) {
        onCreate({ link: formState, createdResponse })
      }
    },
    [formState, onCreate, saveLink],
  )

  const isDisabled = useMemo(
    () => !formState.shortpath.length || !formState.destination.length,
    [formState],
  )

  useEffect(() => {
    if (typeof sp !== 'string') {
      shortInpuRef?.current?.focus()
      return
    }

    destInpuRef?.current?.focus()
    setFormState((state) => ({ ...state, shortpath: sp }))
  }, [sp, destInpuRef, shortInpuRef])

  return (
    <form onSubmit={handleSubmit}>
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: '5fr 8fr',
          gap: '8px',
          gridTemplateAreas: `
            'a b'
            'c c'
          `,
        }}
      >
        <Group>
          <Circle>
            <Typography variant='h3'>{formState.namespace}/</Typography>
          </Circle>
          <TextField
            id='shortpath'
            placeholder='Keyword'
            value={formState.shortpath}
            onChange={handleChange}
            inputRef={shortInpuRef}
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

        <Group>
          <Circle>
            <EastRoundedIcon sx={{ fill: '#fff' }} />
          </Circle>
          <TextField
            id='destination'
            placeholder={isTablet ? 'Paste the link to a resource here' : 'Paste the link here'}
            value={formState.destination}
            onChange={handleChange}
            inputRef={destInpuRef}
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
        <Button
          variant='contained'
          type='submit'
          disabled={isDisabled}
          sx={{
            height: 32,
            gridArea: 'c',
            px: 4,
            typography: 'h3',

            [media.TABLET]: {
              height: 48,
              position: 'absolute',
              right: 80,
            },
            [media.DESKTOP]: {
              height: 64,
              right: 200,
            },
          }}
        >
          Create
        </Button>
      </Box>
    </form>
  )
}
