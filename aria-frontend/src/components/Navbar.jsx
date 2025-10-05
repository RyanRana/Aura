import React from 'react';
import { AppBar, Toolbar, Button, Typography, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

function Navbar() {
  return (
    <AppBar position="static" color="transparent" elevation={0} sx={{ borderBottom: '1px solid #333' }}>
      <Toolbar>
        <Box sx={{ flexGrow: 1 }}>
          <Button component={RouterLink} to="/dashboard" sx={{ color: '#aaa', '&.active': { color: 'white' } }}>
            01 dashboard
          </Button>
          <Button component={RouterLink} to="/chatbox" sx={{ color: '#aaa', '&.active': { color: 'white' } }}>
            02 chatbox
          </Button>
        </Box>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, textAlign: 'center', fontWeight: 'bold' }}>
          AURA
        </Typography>
        <Box sx={{ flexGrow: 1 }} /> {/* Spacer to center AURA */}
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;