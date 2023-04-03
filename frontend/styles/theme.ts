import { createTheme } from '@mui/material/styles'

export const media = {
  TABLET: '@media (min-width: 840px)',
  DESKTOP: '@media (min-width: 1440px)',
}

export const theme = createTheme({
  typography: {
    fontFamily: ['Poppins', 'Sans-serif'].join(', '),
    h1: {
      fontSize: '16px',
      fontWeight: 700,
      lineHeight: '24px',
      [media.TABLET]: {
        fontSize: '20px',
        fontWeight: 700,
        lineHeight: '30px',
      },
      [media.DESKTOP]: {
        fontSize: '24px',
        fontWeight: 700,
        lineHeight: '36px',
      },
    },
    h2: {
      fontSize: '12px',
      lineHeight: '18px',
      [media.TABLET]: {
        fontSize: '14px',
        lineHeight: '21px',
      },
      [media.DESKTOP]: {
        fontSize: '16px',
        lineHeight: '24px',
      },
    },
    h3: {
      fontSize: '10px',
      lineHeight: '15px',
      fontWeight: 700,
      [media.TABLET]: {
        fontSize: '14px',
        fontWeight: 700,
        lineHeight: '21px',
      },
      [media.DESKTOP]: {
        fontSize: '16px',
        fontWeight: 700,
        lineHeight: '24px',
      },
    },
    body1: {
      fontSize: '10px',
      lineHeight: '15px',
      [media.TABLET]: {
        fontSize: '12px',
        lineHeight: '18px',
      },
      [media.DESKTOP]: {
        fontSize: '14px',
        lineHeight: '21px',
      },
    },
    button: {
      fontSize: '12px',
      [media.TABLET]: {
        fontSize: '14px',
      },
      [media.DESKTOP]: {
        fontSize: '16px',
      },
    },
  },
  components: {
    MuiTextField: {
      styleOverrides: {
        root: {
          display: 'flex',
          justifyContent: 'center',
          backgroundColor: '#fff',
          borderRadius: '32px',
          padding: '4px 8px',
          [media.TABLET]: {
            padding: '4px 16px',
          },
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
            fontSize: '10px',
            [media.TABLET]: {
              fontSize: '12px',
            },
            [media.DESKTOP]: {
              fontSize: '14px',
            },
          },
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          margin: '-8px',
        },
      },
    },
    MuiLink: {
      styleOverrides: {
        root: {
          outline: 'none',
          textDecoration: 'none',
          color: '#000000',
        },
      },
    },
    MuiSvgIcon: {
      styleOverrides: {
        root: {
          width: '16px',
          height: '16px',
          fill: 'none',
          [media.TABLET]: {
            width: '24px',
            height: '24px',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          color: '#fff',
          boxShadow: 'none',
          backgroundColor: '#646ae7',
          height: '32px',
          padding: '0 24px',
          borderRadius: '32px',
          textTransform: 'none',
          fontWeight: 400,
          '&:disabled': {
            backgroundColor: '#bdbcf3',
            color: '#fff',
            boxShadow: 'none',
          },
          '&:hover': {
            backgroundColor: '#343AAA',
            color: '#fff',
            boxShadow: 'none',
          },
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          minHeight: 0,
        },
      },
    },
  },
})
