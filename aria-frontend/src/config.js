// API Configuration
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://arua.onrender.com'  // Production backend URL
  : 'http://localhost:5001';

export default API_BASE_URL;
