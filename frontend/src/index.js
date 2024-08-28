import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';

const theme = createTheme({
  palette: {
    mode: 'dark', // Set to dark mode
    primary: {
      main: '#1976d2', // Default MUI primary color
    },
    secondary: {
      main: '#dc004e', // Default MUI secondary color
    },
    background: {
      default: '#121212', // Dark background
      paper: '#1e1e1e', // Slightly lighter background for cards
    },
    text: {
      primary: '#ffffff', // White text for primary
      secondary: '#b0bec5', // Light grey for secondary text
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2rem',
      fontWeight: 700,
    },
    h2: {
      fontSize: '1.5rem',
      fontWeight: 600,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.5,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.4,
    },
  },
  shape: {
    borderRadius: 8, // Rounded corners for cards and buttons
  },
});

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <App />
  </ThemeProvider>,
  document.getElementById('root')
);