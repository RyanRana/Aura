import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';

// Define our custom dark theme
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#4caf50', // A nice green for primary actions
    },
    secondary: {
      main: '#f48fb1',
    },
    background: {
      default: '#121212', // Your desired dark background
      paper: '#1e1e1e',  // Slightly lighter dark for cards/dialogs
    },
    text: {
      primary: '#ffffff',
      secondary: '#aaaaaa',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: 'transparent',
          boxShadow: 'none',
          borderBottom: '1px solid #333',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none', // Prevent ALL CAPS for buttons
        },
      },
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider theme={darkTheme}>
      <CssBaseline /> {/* Provides a consistent baseline for CSS across browsers */}
      <App />
    </ThemeProvider>
  </React.StrictMode>,
);