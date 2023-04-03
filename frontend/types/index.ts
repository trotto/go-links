export * from './link'
export * from './user'
export * from './adminLink'

declare global {
  interface Window {
    _trotto: { defaultNamespace: string; [name: string]: unknown }
  }
}
