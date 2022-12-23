import type { AppProps } from 'next/app'
import '../styles/globals.css'
import styled from '@emotion/styled'
import { NavBar, Footer } from '../components'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import useSWR from 'swr'
import { fetcher } from '../utils/fetcher'
import { User } from '../types'

const Container = styled.div`
  height: 100vh;
`

const Main = styled.div`
  height: calc(100% - 64px - 64px);
`

const theme = createTheme({
  typography: {
    fontFamily: ['Poppins', 'Sans-serif'].join(', '),
  },
  components: {
    // Name of the component
    MuiTextField: {
      styleOverrides: {
        // Name of the slot
        root: {
          display: 'flex',
          justifyContent: 'center',
          backgroundColor: '#fff',
          borderRadius: '32px',
          padding: '4px 16px',
          '& fieldset': { border: 'none' },
          '& input, & .MuiInputBase-root': {
            padding: 0,
          },
          '& input:disabled': {
            color: '#000',
            // NOTE: MUI has this prop
            WebkitTextFillColor: 'unset',
          },
          '& input, & input::placeholder': {
            color: '#000',
            opacity: 1,
          },
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        // Name of the slot
        root: {
          margin: '-8px',
        },
      },
    },
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
  const { data: user } = useSWR(`/_/api/users/me`, fetcher<User>)
  return (
    <ThemeProvider theme={theme}>
      <Container>
        <NavBar user={user} />
        <script src='/_scripts/config.js'></script>
        <Main>
          <Component {...pageProps} user={user} />
        </Main>
        <Footer />
      </Container>
    </ThemeProvider>
  )
}
