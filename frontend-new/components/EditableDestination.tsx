import { Box, Button, IconButton, TextField, Tooltip } from '@mui/material'
import { FC, useState, useCallback, FormEvent, ChangeEvent } from 'react'

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

  const updateLink = useUpdateLink()

  const handleDestinationChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => setDestination(e.target.value),
    [setDestination],
  )
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
          alignItems: 'center,',
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
            placeholder='Keyword'
            value={destination}
            onChange={handleDestinationChange}
            disabled={!editable}
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
        <Tooltip title={disabled && 'You don’t have permission to modify this go link'}>
          <span>
            <IconButton
              onClick={handleEdit}
              sx={{
                opacity: editable ? 1 : 0.25,
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
      </Box>
    </form>
  )
}
