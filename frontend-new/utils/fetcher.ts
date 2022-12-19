declare global {
  interface Window {
    _trotto: {[name: string]: any}
  }
}

export const fetcher = async <T>(url: string, config: RequestInit = {}): Promise<T> => {
  if (config?.method != 'GET')  {
    config = {
      ...config,
      headers: {
        'X-CSRFToken': window._trotto.csrfToken,
        'Content-Type': 'application/json',
        ...config?.headers,
      }
    }
  }
  const res = await fetch(url, config)

  return await res.json()
}