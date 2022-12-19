import { useCallback, useMemo, useState } from 'react'
import useSWR from 'swr'
import Head from 'next/head'
import Image from 'next/image'
import styled from '@emotion/styled'
import { LinkCreationForm } from './components/LinkCreationForm'
import { LinkList } from './components/LinkList'
import { ResponseContainer, ResponseType } from './components/ResponseContaner'
import { Search } from './components/Search'
import { fetcher } from '../../utils/fetcher'
import { Link, LinkCreate, LinkCreateResponse } from '../../types'
import { find } from 'lodash'

const StyledDiv = styled.div`
  background-color: #f2f2f2;
  height: calc(100vh - 64px);
  padding: 64px 200px 0;

  .scrollable {
    height: calc(100% - 176.5px);
    overflow: scroll;
  }
`
interface NotificationState {
  link: Link
  type: ResponseType
  message: string
}

export default function Home() {
  const [notificationState, setNotificationState] = useState<NotificationState>()
  const [searchState, setSearchState] = useState('')
  const { data: links, error, isLoading, mutate } = useSWR('/_/api/links', fetcher<Link[]>)

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
    <StyledDiv>
      <div className='sticky-container'>
        <LinkCreationForm onCreate={handleCreate} />
        {notificationState && <ResponseContainer {...notificationState} />}
        <Search value={searchState} onChange={setSearchState} />
      </div>
      <div className='scrollable'>
        <LinkList links={displayLinks} />
      </div>
    </StyledDiv>
  )
}
