import { useCallback } from 'react'
import useSWR from 'swr'
import { useSWRConfig } from 'swr'

import { User } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

const USERS_API = '/_/api/users/me'

export const useGetMe = () => {
  const { data: user, mutate, isLoading } = useSWR(USERS_API, fetcher<User>)

  return {
    user,
    mutate,
    isLoading,
  }
}

export const useDismissExtensionNotification = () => {
  const { mutate } = useSWRConfig()
  return useCallback(
    () =>
      fetcher<User>(USERS_API, {
        method: 'PUT',
        body: JSON.stringify({ notifications: { install_extension: 'dismissed' } }),
      }).then(() => mutate(USERS_API)),
    [mutate],
  )
}
