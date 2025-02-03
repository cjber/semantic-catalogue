import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#BB86FC', // Light purple for primary elements
    },
    secondary: {
      main: '#03DAC6', // Teal for secondary elements
    },
    background: {
      default: '#121212', // Dark background
      paper: '#1E1E1E', // Slightly lighter background for cards
    },
    text: {
      primary: '#FFFFFF', // White text for primary
      secondary: '#B0BEC5', // Light grey for secondary text
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
    caption: {
      fontSize: '0.75rem',
      lineHeight: 1.2,
    },
  },
  shape: {
    borderRadius: 8, // Rounded corners for cards and buttons
  },
});

export default theme;