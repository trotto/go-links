import styled from '@emotion/styled'
import { Box } from '@mui/material'
import { find } from 'lodash'
import { useCallback, useMemo, useState } from 'react'
import { useEffect } from 'react'
import useSWR from 'swr'

import {
  ExtensionNotification,
  LinkCreationForm,
  LinkList,
  NoLinksNotification,
  ResponseContainer,
  ResponseType,
  Search,
} from 'app/components'
import { Link, LinkCreate, LinkCreateResponse, User } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

const ScrollableArea = styled.div<{ cut: number }>(({ cut }) => ({
  height: `calc(100% - ${cut}px)`,
  overflow: 'scroll',
}))

interface NotificationState {
  link: Link
  type: ResponseType
  message: string
}

interface Props {
  user?: User
}

interface TrottoMetaElement extends HTMLElement {
  content: string
}

export default function Home({ user }: Props) {
  const [notificationState, setNotificationState] = useState<NotificationState>()
  const [searchState, setSearchState] = useState('')
  const [extInstalled, setExtInstalled] = useState(false)
  const { data: links, mutate } = useSWR('/_/api/links', fetcher<Link[]>)

  useEffect(() => {
    const crxInstalledTag = document.getElementsByName(
      'trotto:crxInstalled',
    ) as NodeListOf<TrottoMetaElement>
    const extensionIsInstalled = crxInstalledTag.length > 0 && crxInstalledTag[0].content === 'true'

    setExtInstalled(extensionIsInstalled)
  }, [])

  const handleCreate = useCallback(
    async (link: LinkCreate) => {
      const createdResponse = await fetcher<LinkCreateResponse>('/_/api/links', {
        method: 'POST',
        body: JSON.stringify(link),
      })

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
    return links?.filter((link) => link.shortpath.includes(searchState)) || []
  }, [links, searchState])

  const scrollableAreaCut = useMemo(() => {
    let cut = 168 + 24
    if (notificationState) {
      cut += 209 + 24
    }
    if (!extInstalled) {
      cut += 233 + 40
    }
    return cut
  }, [notificationState, extInstalled])

  return (
    <Box
      sx={{
        backgroundColor: '#fff',
        height: '100%',
        padding: '32px 24px 0',
        '@media (min-width: 840px)': {
          padding: '64px 80px 0',
        },
        '@media (min-width: 1440px)': {
          padding: '64px 200px 0',
        },
      }}
    >
      {!extInstalled && <ExtensionNotification />}
      <Box>
        <LinkCreationForm onCreate={handleCreate} />
        {notificationState && <ResponseContainer {...notificationState} />}
        <Search value={searchState} onChange={setSearchState} />
      </Box>
      {!links || !links.length ? (
        <NoLinksNotification />
      ) : (
        <ScrollableArea cut={scrollableAreaCut}>
          <LinkList links={displayLinks} user={user} />
        </ScrollableArea>
      )}
    </Box>
  )
}
