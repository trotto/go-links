import React from 'react';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import {getConfig} from '../config/index';


const muiTheme = createMuiTheme({
  palette: {
    primary: {
      main: getConfig('palette.primary')
    },
    secondary: {
      main: getConfig('palette.secondary')
    },
    success: {
      main: getConfig('palette.success')
    },
    error: {
      main: getConfig('palette.error')
    }
  },
  typography: {
    fontFamily: [
      'Lato',
      'Helvetica Neue',
      'Helvetica',
      'Arial',
      'sans-serif'
    ],
    button: {
      textTransform: 'none'
    }
  }
});


export const TrottoThemeProvider = ({ children }) => (
  <ThemeProvider theme={muiTheme}>
    {children}
  </ThemeProvider>
)
