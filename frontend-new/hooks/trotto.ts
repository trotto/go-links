interface TrottoCfg {
  isManaged: boolean
}

export const useTrotto: () => TrottoCfg = () => {
  return {
    isManaged: location.host === 'trot.to',
  }
}
