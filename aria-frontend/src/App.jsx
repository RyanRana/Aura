import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { Box, AppBar, Toolbar, Button, Typography } from '@mui/material'; // Typography is still needed for other pages

// IMPORT OUR PAGE COMPONENTS
import Dashboard from './pages/Dashboard';
import Chatbox from './pages/Chatbox';

function App() {
  return (
    <Router>
      <AppBar position="static" color="transparent" elevation={0} sx={{ borderBottom: '1px solid #333' }}>
        <Toolbar>
          {/* Only navigation buttons remain, centered */}
          <Box sx={{ flexGrow: 1, display: 'flex', justifyContent: 'center' }}>
            <Button
              component={NavLink}
              to="/dashboard"
              sx={{ color: '#aaa', '&.active': { color: 'white' }, mr: 1 }}
              end
            >
              01 dashboard
            </Button>
            <Button
              component={NavLink}
              to="/chatbox"
              sx={{ color: '#aaa', '&.active': { color: 'white' } }}
            >
              02 chatbox
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
      
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/chatbox" element={<Chatbox />} />
        <Route path="/" element={<Dashboard />} /> {/* Default route */}
      </Routes>
    </Router>
  );
}

export default App;