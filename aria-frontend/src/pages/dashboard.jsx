import React, { useState, useEffect } from 'react';
import { Box, Container, Typography, Grid, Card, CardContent, List, ListItem, ListItemText, ListItemIcon, CircularProgress } from '@mui/material';
import CircleIcon from '@mui/icons-material/Circle';
import axios from 'axios';

// A reusable card for the KPIs
const KpiCard = ({ title, value }) => (
  <Card sx={{ backgroundColor: '#1e1e1e', height: '100%', minHeight: '120px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
    <CardContent sx={{ p: 3, textAlign: 'center' }}>
      <Typography variant="h4" component="p" sx={{ fontWeight: 'bold' }}>
        {value}
      </Typography>
      <Typography color="text.secondary" sx={{ mt: 1 }}>
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
    <Container maxWidth="lg" sx={{ mt: 4, textAlign: 'center' }}>
      {/* Moved and styled the main titles */}
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold', mb: 1, mt: 4 }}>
        ARIA DASHBOARD {/* Changed back to ARIA as per your screenshot */}
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 6 }}>
        Retail Intelligence & Analytics Dashboard - Real-time Insights from your data.
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={7}>
          <Grid container spacing={3}>
            {kpiData.map((kpi, index) => (
              <Grid item xs={12} sm={6} key={index}> {/* Changed sm to 6 for 2x2 grid */}
                <KpiCard title={kpi.title} value={kpi.value} />
              </Grid>
            ))}
          </Grid>
        </Grid>

        <Grid item xs={12} md={5}>
          <Card sx={{ backgroundColor: '#1e1e1e', textAlign: 'left', p: 1, height: '100%' }}> {/* Ensure card takes full height */}
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
                Recent Sales Activity
              </Typography>
              <List dense>
                {data.recentSales.map((sale, index) => (
                  <ListItem key={index} disablePadding sx={{ borderBottom: index !== data.recentSales.length - 1 ? '1px solid #333' : 'none', py: 1.5 }}>
                    <ListItemIcon sx={{ minWidth: 'auto', mr: 1.5 }}>
                      <CircleIcon sx={{ color: 'primary.main', fontSize: '0.6rem' }} />
                    </ListItemIcon>
                    {/* Removed time from secondary text */}
                    <ListItemText primary={sale.text} secondary={sale.value} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard;