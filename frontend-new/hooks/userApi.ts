import useSWR from 'swr'

import { User } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

export const useGetMe = () => {
  const { data: user, mutate } = useSWR(`/_/api/users/me`, fetcher<User>)

  return {
    user,
    mutate,
  }
}
