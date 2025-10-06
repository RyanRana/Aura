// API Configuration
// Use hostname to detect production since Vercel might not set PROD correctly
const isProduction = typeof window !== 'undefined' && 
  (window.location.hostname.includes('vercel.app') || 
   window.location.hostname.includes('useaura.tech'));

const API_BASE_URL = isProduction || import.meta.env.PROD
  ? 'https://arua.onrender.com'  // Production backend URL
  : 'http://localhost:5001';

console.log('Environment:', import.meta.env.MODE, 'API URL:', API_BASE_URL);

export default API_BASE_URL;
