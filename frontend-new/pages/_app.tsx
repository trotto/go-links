import { Global } from '@emotion/react'
import { Box } from '@mui/material'
import { ThemeProvider } from '@mui/material/styles'
import type { AppProps } from 'next/app'

import { Footer, NavBar } from 'app/components'
import { Context } from 'app/context'
import { useGetMe } from 'app/hooks'
import { theme, globalStyles } from 'app/styles'

export default function App({ Component, pageProps }: AppProps) {
  const { user } = useGetMe()
  return (
    <Context.Provider value={{ user }}>
      <ThemeProvider theme={theme}>
        <Global styles={globalStyles} />
        <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
          <NavBar />
          <Box sx={{ overflow: 'hidden', flexGrow: 1 }}>
            <Component {...pageProps} />
          </Box>
          <Footer />
        </Box>
      </ThemeProvider>
    </Context.Provider>
  )
}
