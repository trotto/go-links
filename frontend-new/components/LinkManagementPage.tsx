import { Box } from '@mui/material'
import { FC } from 'react'

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

export const LinkManagementPage: FC = () => {
  const {
    notificationState,
    extensionInstalled,
    filterValue,
    setFilterValue,
    displayLinks,
    onSave,
    linksExists,
    noLinks,
  } = useLinkList()

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
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
        <LinkCreationForm onCreate={onSave} onTyping={setFilterValue} />
        {notificationState && <ResponseContainer {...notificationState} />}
        {noLinks && <NoLinksNotification />}
        <Search value={filterValue} onChange={setFilterValue} />
      </Box>
      {linksExists && <LinkList links={displayLinks} />}
    </Box>
  )
}
