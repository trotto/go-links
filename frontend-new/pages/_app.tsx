import styled from '@emotion/styled'
import { ThemeProvider } from '@mui/material/styles'
import type { AppProps } from 'next/app'
import 'styles/globals.css'

import { Footer, NavBar } from 'app/components'
import { useGetMe } from 'app/hooks'
import { theme } from 'app/styles/theme'

const Container = styled.div`
  height: 100vh;
`

const Main = styled.div`
  height: calc(100% - 64px - 64px);
`

export default function App({ Component, pageProps }: AppProps) {
  const { user } = useGetMe()
  return (
    <ThemeProvider theme={theme}>
      <Container>
        <NavBar user={user} />
        <Main>
          <Component {...pageProps} user={user} />
        </Main>
        <Footer />
      </Container>
    </ThemeProvider>
  )
}
