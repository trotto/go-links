import useSWR from 'swr'

import { AdminLink } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

export const useGetAdminLinks = () => {
  const { data: adminLinks, mutate } = useSWR(`/_admin_links`, fetcher<AdminLink[]>)
  return {
    adminLinks,
    mutate,
  }
}
