import { useState, useEffect } from 'react'

const BASE_DOMAIN = 'trot.to'

interface TrottoCfg {
  isManaged: boolean
  isExtensionInstalled: boolean
  baseUrl: string
}

interface TrottoMetaElement extends HTMLElement {
  content: string
}

export const useTrotto: () => TrottoCfg = () => {
  const [isExtensionInstalled, setIsExtensionInstalled] = useState(false)
  const [isManaged, setIsManaged] = useState(false)
  const [baseUrl, setBaseUrl] = useState(`https://${BASE_DOMAIN}`)

  useEffect(() => {
    const crxInstalledTag = document.getElementsByName(
      'trotto:crxInstalled',
    ) as NodeListOf<TrottoMetaElement>
    const extensionIsInstalled = crxInstalledTag.length > 0 && crxInstalledTag[0].content === 'true'

    setIsExtensionInstalled(extensionIsInstalled)

    if (!location) {
      return
    }

    setIsManaged(location.host === BASE_DOMAIN)

    if (isExtensionInstalled) {
      return setBaseUrl('http://go')
    }

    if (location.host.indexOf('localhost') === 0) {
      return setBaseUrl('http://localhost:9095')
    }

    return setBaseUrl(location.origin)
  }, [isExtensionInstalled])

  return {
    isManaged,
    isExtensionInstalled,
    baseUrl,
  }
}
