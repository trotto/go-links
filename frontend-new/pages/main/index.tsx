import styled from '@emotion/styled'
import { Box } from '@mui/material'
import { find } from 'lodash'
import { useCallback, useMemo, useState } from 'react'
import useSWR from 'swr'

import { Link, LinkCreate, LinkCreateResponse, User } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

import { LinkCreationForm } from './components/LinkCreationForm'
import { LinkList } from './components/LinkList'
import { ResponseContainer, ResponseType } from './components/ResponseContaner'
import { Search } from './components/Search'

const Container = styled.div`
  background-color: #fff;
  height: calc(100%);
  padding: 64px 200px 0;
`

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

export default function Home({ user }: Props) {
  const [notificationState, setNotificationState] = useState<NotificationState>()
  const [searchState, setSearchState] = useState('')
  const { data: links, mutate } = useSWR('/_/api/links', fetcher<Link[]>)

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

  return (
    <Container>
      <Box>
        <LinkCreationForm onCreate={handleCreate} />
        {notificationState && <ResponseContainer {...notificationState} />}
        <Search value={searchState} onChange={setSearchState} />
      </Box>
      <ScrollableArea cut={notificationState ? 168 + 24 + 209 + 24 : 168 + 24}>
        <LinkList links={displayLinks} user={user} />
      </ScrollableArea>
    </Container>
  )
}
