import React, { useState, useEffect } from 'react';
import { Box, Container, Typography, Grid, Card, CardContent, List, ListItem, ListItemText, ListItemIcon, CircularProgress } from '@mui/material';
import CircleIcon from '@mui/icons-material/Circle';
import axios from 'axios';

// A reusable card for the KPIs
const KpiCard = ({ title, value }) => (
  <Card sx={{ 
    backgroundColor: '#1e1e1e', 
    height: '100%', 
    minHeight: '160px', 
    display: 'flex', 
    alignItems: 'center', 
    justifyContent: 'center',
    border: '1px solid #333',
    transition: 'transform 0.2s, border-color 0.2s',
    '&:hover': {
      transform: 'translateY(-4px)',
      borderColor: '#8b5cf6'
    }
  }}>
    <CardContent sx={{ p: 4, textAlign: 'center', width: '100%' }}>
      <Typography variant="h3" component="p" sx={{ fontWeight: 'bold', color: '#fff', mb: 2 }}>
        {value}
      </Typography>
      <Typography sx={{ color: '#aaa', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
        {title}
      </Typography>
    </CardContent>
  </Card>
);

function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get('http://localhost:5001/api/dashboard-data');
        setData(response.data);
      } catch (err) {
        setError('Failed to load dashboard data. Please ensure the backend is running and connected to Snowflake.');
        console.error("Dashboard data fetch error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}><CircularProgress /></Box>;
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 8, textAlign: 'center' }}>
        <Typography variant="h5" color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Check your network connection and ensure your Flask backend server is running correctly.
        </Typography>
      </Container>
    );
  }

  const kpiData = [
    { title: 'TOTAL REVENUE (7D)', value: data.totalRevenue, size: 6 },
    { title: 'UNITS SOLD (7D)', value: data.unitsSold, size: 6 },
    { title: 'AVG PROFIT MARGIN', value: data.avgProfitMargin, size: 6 },
    { title: 'TOP PRODUCT', value: data.topProduct, size: 6 },
  ];

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4, px: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" sx={{ fontWeight: 'bold', mb: 1, color: '#fff' }}>
          AURA DASHBOARD
        </Typography>
        <Typography variant="body1" sx={{ color: '#aaa', fontSize: '1rem' }}>
          Retail Intelligence & Analytics Dashboard - Real-time Insights from your data.
        </Typography>
      </Box>

      {/* KPI Cards Grid */}
      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 3, mb: 3 }}>
        {kpiData.map((kpi, index) => (
          <KpiCard key={index} title={kpi.title} value={kpi.value} />
        ))}
      </Box>

      {/* Recent Sales Activity */}
      <Card sx={{ backgroundColor: '#1e1e1e', border: '1px solid #333' }}>
        <CardContent sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, color: '#fff' }}>
            📋 Recent Sales Activity
          </Typography>
          <List sx={{ py: 0 }}>
            {data.recentSales.map((sale, index) => (
              <ListItem 
                key={index} 
                sx={{ 
                  borderBottom: index !== data.recentSales.length - 1 ? '1px solid #333' : 'none', 
                  py: 1.5,
                  px: 2,
                  '&:hover': { backgroundColor: '#252525' }
                }}
              >
                <ListItemIcon sx={{ minWidth: 'auto', mr: 2 }}>
                  <CircleIcon sx={{ color: '#8b5cf6', fontSize: '0.7rem' }} />
                </ListItemIcon>
                <ListItemText 
                  primary={sale.text} 
                  secondary={sale.value}
                  primaryTypographyProps={{ sx: { color: '#fff', fontSize: '0.95rem' } }}
                  secondaryTypographyProps={{ sx: { color: '#10b981', fontWeight: 600, fontSize: '0.9rem' } }}
                />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
    </Container>
  );
}

export default Dashboard;