import { Box } from '@mui/material'
import { useRouter } from 'next/router'
import { FC, useCallback } from 'react'

import {
  ExtensionNotification,
  LinkCreationForm,
  LinkList,
  NoLinksNotification,
  ResponseContainer,
  Search,
  TransferConfirmModal,
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
    transferState,
  } = useLinkList()

  const router = useRouter()

  const handleClose = useCallback(() => {
    router.push(router.pathname, undefined, { shallow: true })
  }, [router])

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
      {transferState?.link && transferState?.token && (
        <TransferConfirmModal
          link={transferState?.link}
          open={!!transferState?.link}
          onClose={handleClose}
          transferToken={transferState.token}
        />
      )}
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
