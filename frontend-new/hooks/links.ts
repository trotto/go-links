import { find } from 'lodash'
import { useCallback, useMemo, useState, useEffect } from 'react'

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

interface TrottoMetaElement extends HTMLElement {
  content: string
}

export const useLinkList = () => {
  const [notificationState, setNotificationState] = useState<NotificationState>()
  const [filterValue, setFilterValue] = useState('')
  const [extensionInstalled, setExtensionInstalled] = useState(false)
  const { links, mutate } = useGetLinkList()

  useEffect(() => {
    const crxInstalledTag = document.getElementsByName(
      'trotto:crxInstalled',
    ) as NodeListOf<TrottoMetaElement>
    const extensionIsInstalled = crxInstalledTag.length > 0 && crxInstalledTag[0].content === 'true'

    setExtensionInstalled(extensionIsInstalled)
  }, [])

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

  const displayLinks = useMemo(() => {
    return links?.filter((link) => link.shortpath.includes(filterValue)) || []
  }, [links, filterValue])

  return {
    notificationState,
    extensionInstalled,
    filterValue,
    setFilterValue,
    links,
    displayLinks,
    onSave,
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
