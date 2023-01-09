import { useCallback } from 'react'
import { useSWRConfig } from 'swr'
import useSWR from 'swr'

import { Link, LinkCreate, LinkUpdate, LinkCreateResponse } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

export const useGetLinkList = () => {
  const { data: links, mutate, isLoading } = useSWR('/_/api/links', fetcher<Link[]>)

  return {
    links,
    mutate,
    isLoading,
  }
}

export const useSaveLink = () => {
  return useCallback(
    (link: LinkCreate) =>
      fetcher<LinkCreateResponse>('/_/api/links', {
        method: 'POST',
        body: JSON.stringify(link),
      }),
    [],
  )
}

export const useUpdateLink = () => {
  const { mutate } = useSWRConfig()

  return useCallback(
    (id: number, link: LinkUpdate) =>
      fetcher<Link>(`/_/api/links/${id}`, {
        method: 'PUT',
        body: JSON.stringify(link),
      }).then(() => mutate('/_/api/links')),
    [mutate],
  )
}

export const useDeleteLink = () => {
  const { mutate } = useSWRConfig()

  return useCallback(
    (id: number) =>
      fetcher<void>(`/_/api/links/${id}`, {
        method: 'DELETE',
      }).then(() => mutate('/_/api/links')),
    [mutate],
  )
}

interface TransferToken {
  url: string
}

export const useGetTransferToken = (id: number) => {
  const { data: transferToken } = useSWR(`/_/api/links/${id}/transfer_link`, (url) =>
    fetcher<TransferToken>(url, { method: 'POST' }),
  )

  return transferToken
}
