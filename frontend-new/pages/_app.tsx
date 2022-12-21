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
  components: {
    // Name of the component
    MuiButton: {
      styleOverrides: {
        // Name of the slot
        root: {
          // Some CSS
          color: '#fff',
          backgroundColor: '#646ae7',
          height: '32px',
          padding: '0 24px',
          borderRadius: '32px',
          textTransform: 'none',
          fontSize: '16px',
          fontWeight: 400,
          '&:disabled': {
            backgroundColor: '#bdbcf3',
            color: '#fff',
          },
          '&:hover': {
            backgroundColor: '#bdbcf3',
            color: '#fff',
          },
        },
      },
    },
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
