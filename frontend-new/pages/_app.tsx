import type { AppProps } from 'next/app'
import '../styles/globals.css'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div>
      <script src='/_scripts/config.js'></script>
      <script src='/_scripts/config2.js'></script>
      <Component {...pageProps} />
    </div>
  )
}
