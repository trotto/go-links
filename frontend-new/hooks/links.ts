import { find, some } from 'lodash'
import { map, pipe, includes } from 'lodash/fp'
import { useCallback, useMemo, useState } from 'react'

import { Link, LinkCreate, LinkCreateResponse } from 'app/types'

import { useGetLinkList } from './linksApi'

enum ResponseType {
  SUCCESS = 'success',
  ERROR = 'error',
}

interface NotificationState {
  link: Link
  type: ResponseType
  message: string
}

export const useLinkList = () => {
  const [notificationState, setNotificationState] = useState<NotificationState>()
  const [filterValue, setFilterValue] = useState('')
  const { links, mutate, isLoading } = useGetLinkList()

  const onSave = useCallback(
    async ({
      link,
      createdResponse,
    }: {
      link: LinkCreate
      createdResponse: LinkCreateResponse
    }) => {
      if (createdResponse.error) {
        const conflictLink = find(links, ['shortpath', link.shortpath])
        if (!conflictLink) {
          return
        }

        return setNotificationState({
          link: conflictLink,
          type: ResponseType.ERROR,
          message: 'That go link already exists:',
        })
      }
      setNotificationState({
        link: createdResponse,
        type: ResponseType.SUCCESS,
        message: 'Success! New go link created:',
      })
      mutate()
    },
    [mutate, links, setNotificationState],
  )

  const displayLinks = useMemo(
    () =>
      links?.filter(
        pipe(
          ({ shortpath, destination_url, owner }) => [shortpath, destination_url, owner],
          map(includes(filterValue)),
          some,
        ),
      ),
    [links, filterValue],
  )

  const linksExists = useMemo(() => !isLoading && links && !!links.length, [isLoading, links])
  const noLinks = useMemo(() => !isLoading && !(links && links.length), [isLoading, links])

  return {
    notificationState,
    filterValue,
    setFilterValue,
    links,
    displayLinks,
    onSave,
    linksExists,
    noLinks,
  }
}

export const useFullShortPath = ({
  shortpath,
  namespace = window._trotto.defaultNamespace,
}: {
  shortpath: string
  namespace?: string
}) => useMemo(() => `${namespace}/${shortpath}`, [namespace, shortpath])

export const useEditableDestination = (id: number, destinationUrl: string) => {
  const [destination, setDestination] = useState(destinationUrl)
  const [editable, setEditable] = useState(false)

  const toggleEditMode = useCallback(() => setEditable((editable) => !editable), [setEditable])

  return {
    destination,
    setDestination,
    editable,
    toggleEditMode,
  }
}
