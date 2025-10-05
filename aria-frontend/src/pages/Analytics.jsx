import React, { useState, useEffect } from 'react';
import { Box, Container, Typography, Grid, Card, CardContent, CircularProgress } from '@mui/material';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

// Color palette matching your dark theme
const COLORS = ['#8b5cf6', '#ec4899', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'];

function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get('http://localhost:5001/api/analytics-data');
        setData(response.data);
      } catch (err) {
        setError('Failed to load analytics data. Please ensure the backend is running.');
        console.error("Analytics data fetch error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress sx={{ color: '#8b5cf6' }} />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 8, textAlign: 'center' }}>
        <Typography variant="h5" color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      </Container>
    );
  }

  // Custom tooltip styling
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <Box sx={{ backgroundColor: '#1e1e1e', border: '1px solid #8b5cf6', p: 1.5, borderRadius: 1 }}>
          <Typography variant="body2" sx={{ color: '#fff', mb: 0.5 }}>{label}</Typography>
          {payload.map((entry, index) => (
            <Typography key={index} variant="body2" sx={{ color: entry.color }}>
              {entry.name}: {entry.value}
            </Typography>
          ))}
        </Box>
      );
    }
    return null;
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 6, mb: 6 }}>
      {/* Header */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="h3" sx={{ fontWeight: 'bold', mb: 2, color: '#fff' }}>
          📊 Analytics Dashboard
        </Typography>
        <Typography variant="body1" sx={{ color: '#aaa', fontSize: '1.1rem' }}>
          Real-time insights from your retail data warehouse
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {/* Sales Trend Line Chart */}
        <Grid item xs={12}>
          <Card sx={{ backgroundColor: '#1e1e1e', height: '550px', border: '1px solid #333' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 3, color: '#fff', fontWeight: 600 }}>
                📈 Sales Trend (Last 30 Days)
              </Typography>
              <ResponsiveContainer width="100%" height={460}>
                <AreaChart data={data?.salesTrend || []}>
                  <defs>
                    <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis dataKey="date" stroke="#aaa" />
                  <YAxis stroke="#aaa" />
                  <Tooltip content={<CustomTooltip />} />
                  <Area type="monotone" dataKey="sales" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorSales)" />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Top Products Pie Chart */}
        <Grid item xs={12}>
          <Card sx={{ backgroundColor: '#1e1e1e', height: '550px', border: '1px solid #333' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 3, color: '#fff', fontWeight: 600 }}>
                🥇 Top Products by Revenue
              </Typography>
              <ResponsiveContainer width="100%" height={460}>
                <PieChart>
                  <Pie
                    data={data?.topProducts || []}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={120}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {(data?.topProducts || []).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Store Performance Bar Chart */}
        <Grid item xs={12}>
          <Card sx={{ backgroundColor: '#1e1e1e', height: '550px', border: '1px solid #333' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 3, color: '#fff', fontWeight: 600 }}>
                🏪 Store Performance
              </Typography>
              <ResponsiveContainer width="100%" height={460}>
                <BarChart data={data?.storePerformance || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis dataKey="store" stroke="#aaa" />
                  <YAxis stroke="#aaa" />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="revenue" fill="#06b6d4" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Daily Sales Volume */}
        <Grid item xs={12}>
          <Card sx={{ backgroundColor: '#1e1e1e', height: '550px', border: '1px solid #333' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 3, color: '#fff', fontWeight: 600 }}>
                📦 Daily Sales Volume
              </Typography>
              <ResponsiveContainer width="100%" height={460}>
                <LineChart data={data?.spoilageData || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis dataKey="date" stroke="#aaa" />
                  <YAxis stroke="#aaa" />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Line type="monotone" dataKey="quantity" name="Units Sold" stroke="#ef4444" strokeWidth={2} dot={{ r: 4 }} />
                  <Line type="monotone" dataKey="value" name="Revenue" stroke="#f59e0b" strokeWidth={2} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Category Sales Comparison */}
        <Grid item xs={12}>
          <Card sx={{ backgroundColor: '#1e1e1e', height: '550px', border: '1px solid #333' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 3, color: '#fff', fontWeight: 600 }}>
                📦 Top Products Comparison
              </Typography>
              <ResponsiveContainer width="100%" height={460}>
                <BarChart data={data?.categoryComparison || []} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis type="number" stroke="#aaa" />
                  <YAxis dataKey="category" type="category" stroke="#aaa" width={150} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="sales" fill="#10b981" radius={[0, 8, 8, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Promotion Effectiveness */}
        <Grid item xs={12}>
          <Card sx={{ backgroundColor: '#1e1e1e', height: '550px', border: '1px solid #333' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 3, color: '#fff', fontWeight: 600 }}>
                🎯 Sales with vs without Promotions
              </Typography>
              <ResponsiveContainer width="100%" height={460}>
                <BarChart data={data?.promotionEffectiveness || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis dataKey="promotion" stroke="#aaa" />
                  <YAxis stroke="#aaa" />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Bar dataKey="withPromo" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
                  <Bar dataKey="withoutPromo" fill="#6b7280" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Analytics;
