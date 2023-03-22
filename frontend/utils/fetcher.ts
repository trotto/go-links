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

  return await res.json()
}
