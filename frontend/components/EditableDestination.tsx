import CloseRoundedIcon from '@mui/icons-material/CloseRounded'
import { Box, Button, IconButton, TextField, Tooltip } from '@mui/material'
import { FC, useState, useCallback, FormEvent, ChangeEvent, useRef, useEffect } from 'react'

import { useUpdateLink } from 'app/hooks'
import { Edit } from 'app/icons'
import { media } from 'app/styles/theme'

interface Props {
  id: number
  destinationUrl: string
  disabled: boolean
}

export const EditableDestination: FC<Props> = ({ id, destinationUrl, disabled }) => {
  const [destination, setDestination] = useState(destinationUrl)
  const [editable, setEditable] = useState(false)
  const destInpuRef = useRef<HTMLInputElement>(null)

  const updateLink = useUpdateLink()

  const handleDestinationChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => setDestination(e.target.value),
    [],
  )

  useEffect(() => {
    if (!editable) {
      return
    }
    destInpuRef?.current?.select()
    destInpuRef?.current?.focus()
  }, [editable])

  const handleEdit = useCallback(() => setEditable((editable) => !editable), [setEditable])

  const handleSave = useCallback(
    (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault()
      updateLink(id, { destination })
      handleEdit()
    },
    [destination, id, handleEdit, updateLink],
  )
  return (
    <form onSubmit={handleSave}>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            borderRadius: '32px',
            background: '#fff',
            mr: 1,
            flexGrow: 1,

            [media.TABLET]: {
              mr: 3,
            },
          }}
        >
          <TextField
            id='destination'
            placeholder='Paste the link to a resource here'
            value={destination}
            onChange={handleDestinationChange}
            disabled={!editable}
            inputRef={destInpuRef}
            sx={{
              height: 24,
              flexGrow: 1,
              [media.TABLET]: {
                height: 32,
              },
            }}
          />
          {editable && (
            <Button
              className='button'
              variant='contained'
              type='submit'
              sx={{
                backgroundColor: '#000',
                height: 24,
                [media.TABLET]: {
                  height: 32,
                },

                '&:hover': {
                  backgroundColor: '#5F5F5F',
                },
              }}
            >
              Save
            </Button>
          )}
        </Box>
        {editable ? (
          <IconButton
            onClick={handleEdit}
            sx={{
              height: 32,
              [media.TABLET]: {
                height: 40,
              },
            }}
          >
            <CloseRoundedIcon sx={{ fill: '#000' }} />
          </IconButton>
        ) : (
          <Tooltip title={disabled && 'You don’t have permission to modify this go link'}>
            <span>
              <IconButton
                onClick={handleEdit}
                sx={{
                  opacity: 1,
                  '&:disabled': {
                    opacity: 0.1,
                  },
                }}
                disabled={disabled}
              >
                <Edit />
              </IconButton>
            </span>
          </Tooltip>
        )}
      </Box>
    </form>
  )
}
