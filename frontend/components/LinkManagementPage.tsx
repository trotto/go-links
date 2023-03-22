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
import { useLinkList, useTrotto } from 'app/hooks'
import { media } from 'app/styles/theme'

export const LinkManagementPage: FC = () => {
  const {
    notificationState,
    filterValue,
    setFilterValue,
    displayLinks,
    onSave,
    noLinks,
    isLoading,
  } = useLinkList()

  const { isExtensionInstalled } = useTrotto()

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
      {!isExtensionInstalled && <ExtensionNotification />}
      <Box>
        <LinkCreationForm onCreate={onSave} onTyping={setFilterValue} />
        {notificationState && <ResponseContainer {...notificationState} />}
        {noLinks && <NoLinksNotification />}
        <Search value={filterValue} onChange={setFilterValue} />
      </Box>
      <LinkList links={displayLinks} isLoading={isLoading} />
    </Box>
  )
}
