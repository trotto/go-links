import { useSnackbar } from 'notistack'
import { useCallback } from 'react'

import { fetcher } from 'app/utils/fetcher'

const TRANSFER_LINK_API = '/_/api/transfer_link/'

export const useTransferConfirm = (token: string, fullShortPath: string) => {
  const { enqueueSnackbar } = useSnackbar()
  return useCallback(
    () =>
      fetcher<null>(`${TRANSFER_LINK_API}/${token}`, {
        method: 'POST',
        body: null,
      })
        .then(() => {
          enqueueSnackbar(`You've taken ownership of ${fullShortPath}`, { variant: 'success' })
        })
        .catch((err) => {
          enqueueSnackbar(err.message || 'Something went wrong. Ownership transfer failed.', {
            variant: 'error',
          })
        }),
    [enqueueSnackbar, token, fullShortPath],
  )
}
