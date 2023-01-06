import styled from '@emotion/styled'
import { Box } from '@mui/material'
import { useMemo } from 'react'

import {
  ExtensionNotification,
  LinkCreationForm,
  LinkList,
  NoLinksNotification,
  ResponseContainer,
  Search,
} from 'app/components'
import { useLinkList } from 'app/hooks/links'
import { media } from 'app/styles/theme'
import { User } from 'app/types'

const ScrollableArea = styled.div<{ cut: number }>(({ cut }) => ({
  height: `calc(100% - ${cut}px)`,
  overflow: 'scroll',
}))

interface Props {
  user?: User
}

export default function Home({ user }: Props) {
  const {
    notificationState,
    extensionInstalled,
    filterValue,
    setFilterValue,
    links,
    displayLinks,
    onSave,
  } = useLinkList()

  const scrollableAreaCut = useMemo(() => {
    let cut = 168 + 24
    if (notificationState) {
      cut += 209 + 24
    }
    if (!extensionInstalled) {
      cut += 233 + 40
    }
    return cut
  }, [notificationState, extensionInstalled])

  return (
    <Box
      sx={{
        backgroundColor: '#fff',
        height: '100%',
        pt: 4,
        px: 3,
        [media.TABLET]: {
          pt: 8,
          px: 10,
        },
        [media.DESKTOP]: {
          px: 25,
        },
      }}
    >
      {!extensionInstalled && <ExtensionNotification />}
      <Box>
        <LinkCreationForm onCreate={onSave} />
        {notificationState && <ResponseContainer {...notificationState} />}
        {(!links || !links.length) && <NoLinksNotification />}
        <Search value={filterValue} onChange={setFilterValue} />
      </Box>
      {links && !!links.length && (
        <ScrollableArea cut={scrollableAreaCut}>
          <LinkList links={displayLinks} user={user} />
        </ScrollableArea>
      )}
    </Box>
  )
}
