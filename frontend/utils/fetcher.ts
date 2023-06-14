let csrfToken: string

export const fetcher = async <T>(url: string, config: RequestInit = {}): Promise<T> => {
  if (config?.method != 'GET') {
    if (!csrfToken) {
      const response = await (await fetch('/_csrf_token')).json()
      csrfToken = response.csrfToken
    }
    config = {
      ...config,
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
        ...config?.headers,
      },
    }
  }
  const res = await fetch(url, config)

  if (res.status >= 400) {
    throw new Error((await res.json()).error)
  }

  try {
    return await res.json()
  } catch (error) {
    return null as T
  }
}
