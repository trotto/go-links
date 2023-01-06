export * from './link'
export * from './user'

declare global {
  interface Window {
    _trotto: { [name: string]: unknown }
  }
}
