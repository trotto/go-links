import { Box } from '@mui/material'
import { ThemeProvider } from '@mui/material/styles'
import type { AppProps } from 'next/app'
import 'styles/globals.css'

import { Footer, NavBar } from 'app/components'
import { useGetMe } from 'app/hooks'
import { theme } from 'app/styles/theme'

export default function App({ Component, pageProps }: AppProps) {
  const { user } = useGetMe()
  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
        <NavBar user={user} />
        <Box sx={{ overflow: 'hidden', flexGrow: 1 }}>
          <Component {...pageProps} user={user} />
        </Box>
        <Footer />
      </Box>
    </ThemeProvider>
  )
}
