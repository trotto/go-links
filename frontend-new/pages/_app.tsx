import type { AppProps } from 'next/app'
import '../styles/globals.css'
import styled from '@emotion/styled'
import { NavBar, Footer } from '../components'
import { ThemeProvider, createTheme } from '@mui/material/styles'

const StyledDiv = styled.div`
  height: 100vh;

  .main {
    height: calc(100% - 64px - 64px);
  }
`

const theme = createTheme({
  typography: {
    fontFamily: ['Poppins', 'Sans-serif'].join(', '),
  },
})

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider theme={theme}>
      <StyledDiv>
        <NavBar />
        <script src='/_scripts/config.js'></script>
        <div className='main'>
          <Component {...pageProps} />
        </div>
        <Footer />
      </StyledDiv>
    </ThemeProvider>
  )
}
