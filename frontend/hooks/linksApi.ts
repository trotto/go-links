import { useSnackbar } from 'notistack'
import { useCallback } from 'react'
import { useSWRConfig } from 'swr'
import useSWR from 'swr'

import { Link, LinkCreate, LinkUpdate, LinkCreateResponse } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

const LINKS_API = '/_/api/links'

export const useGetLinkList = () => {
  const { data: links, mutate, isLoading } = useSWR(LINKS_API, fetcher<Link[]>)

  return {
    links,
    mutate,
    isLoading,
  }
}

export const useSaveLink = () => {
  const { enqueueSnackbar } = useSnackbar()
  return useCallback(
    (link: LinkCreate) =>
      fetcher<LinkCreateResponse>(LINKS_API, {
        method: 'POST',
        body: JSON.stringify(link),
      })
        .then((res) => {
          if (res && res.error && !res.error.startsWith('That go link already exists.')) {
            enqueueSnackbar(res.error, { variant: 'error' })

            return
          }

          return res
        })
        .catch(() => {
          enqueueSnackbar('Something went wrong. Link was not created.', { variant: 'error' })
        }),
    [enqueueSnackbar],
  )
}

export const useGetSuggestedLinks = () => {
  const quantity = 5
  const similarityThreshold = 0.5

  return useCallback(
    (similarTo: string) =>
      fetcher<Link[]>(
        `${LINKS_API}?similar_to=${similarTo}&limit=${quantity}&similarity_threshold=${similarityThreshold}`,
        { method: 'GET' },
      ),
    [quantity, similarityThreshold],
  )
}

export const useUpdateLink = () => {
  const { mutate } = useSWRConfig()
  const { enqueueSnackbar } = useSnackbar()

  return useCallback(
    (id: number, link: LinkUpdate) =>
      fetcher<Link>(`${LINKS_API}/${id}`, {
        method: 'PUT',
        body: JSON.stringify(link),
      })
        .then(() => mutate(LINKS_API))
        .catch(() => {
          enqueueSnackbar('Something went wrong. Link was not updated.', { variant: 'error' })
        }),
    [mutate, enqueueSnackbar],
  )
}

export const useDeleteLink = () => {
  const { mutate } = useSWRConfig()
  const { enqueueSnackbar } = useSnackbar()

  return useCallback(
    (id: number) =>
      fetcher<void>(`${LINKS_API}/${id}`, {
        method: 'DELETE',
      })
        .then(() => mutate(LINKS_API))
        .catch(() => {
          enqueueSnackbar('Something went wrong. Link was not deleted.', { variant: 'error' })
        }),
    [mutate, enqueueSnackbar],
  )
}

interface TransferToken {
  url: string
}

export const useGetTransferToken = (id: number) => {
  const { data: transferToken } = useSWR(`${LINKS_API}/${id}/transfer_link`, (url) =>
    fetcher<TransferToken>(url, { method: 'POST' }),
  )

  return transferToken
}
