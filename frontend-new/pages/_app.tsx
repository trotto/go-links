import styled from '@emotion/styled'
import { ThemeProvider } from '@mui/material/styles'
import type { AppProps } from 'next/app'
import 'styles/globals.css'
import useSWR from 'swr'

import { Footer, NavBar } from 'app/components'
import { theme } from 'app/styles/theme'
import { User } from 'app/types'
import { fetcher } from 'app/utils/fetcher'

const Container = styled.div`
  height: 100vh;
`

const Main = styled.div`
  height: calc(100% - 64px - 64px);
`

export default function App({ Component, pageProps }: AppProps) {
  const { data: user } = useSWR(`/_/api/users/me`, fetcher<User>)
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
