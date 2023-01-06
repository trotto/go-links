export * from './link'
export * from './user'

declare global {
  interface Window {
    _trotto: { defaultNamespace: string; [name: string]: unknown }
  }
}
