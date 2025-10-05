# 🚀 Backend Deployment Guide

## Quick Steps to Deploy Backend

### **Option 1: Render (Recommended - Free Tier Available)**

1. **Go to Render:** https://render.com
2. **Sign up** with GitHub
3. Click **"New +"** → **"Web Service"**
4. **Connect Repository:** `RyanRana/hackrufall25`
5. **Configure:**
   ```
   Name: aura-backend
   Region: Oregon (US West)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python api.py
   Instance Type: Free
   ```

6. **Environment Variables** (Click "Advanced"):
   ```
   SNOWFLAKE_USER = your_value
   SNOWFLAKE_PASSWORD = your_value
   SNOWFLAKE_ACCOUNT = your_value
   SNOWFLAKE_WAREHOUSE = your_value
   SNOWFLAKE_DATABASE = your_value
   SNOWFLAKE_SCHEMA = your_value
   GOOGLE_API_KEY = your_value
   ```

7. Click **"Create Web Service"**
8. **Copy your backend URL** (e.g., `https://aura-backend.onrender.com`)

---

### **Option 2: Railway**

1. **Go to Railway:** https://railway.app
2. Click **"Start a New Project"** → **"Deploy from GitHub repo"**
3. Select `RyanRana/hackrufall25`
4. Railway auto-detects Python
5. **Add environment variables** in Settings
6. **Set Root Directory:** `backend`
7. **Copy your backend URL**

---

## 📝 Update Frontend After Backend Deployment

### **Step 1: Update config.js**

Edit `/aria-frontend/src/config.js`:

```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://aura-backend.onrender.com'  // ← Replace with YOUR backend URL
  : 'http://localhost:5001';

export default API_BASE_URL;
```

### **Step 2: Update all API calls**

You need to update these files to use the config:

#### **dashboard.jsx**
```javascript
import API_BASE_URL from '../config';

// Change:
const response = await axios.get('http://localhost:5001/api/dashboard-data');

// To:
const response = await axios.get(`${API_BASE_URL}/api/dashboard-data`);
```

#### **Analytics.jsx**
```javascript
import API_BASE_URL from '../config';

// Change:
const response = await axios.get('http://localhost:5001/api/analytics-data');

// To:
const response = await axios.get(`${API_BASE_URL}/api/analytics-data`);
```

#### **Chatbox.jsx**
```javascript
import API_BASE_URL from '../config';

// Update all axios calls to use API_BASE_URL
```

### **Step 3: Commit and Push**

```bash
git add .
git commit -m "Update API URLs for production backend"
git push origin main
```

Vercel will automatically redeploy with the new backend URL!

---

## ⚠️ Important: Update Flask for Production

Edit `backend/api.py` to allow production domain:

```python
# Change:
CORS(app, resources={r"/api/*": {"origins": "*"}})

# To (more secure):
CORS(app, resources={r"/api/*": {
    "origins": [
        "http://localhost:5173",
        "https://useaura.tech",
        "https://www.useaura.tech",
        "https://hackrufall25.vercel.app"
    ]
}})
```

Also update the Flask app to run on the correct port for Render:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
```

---

## ✅ Testing

After deployment:

1. Visit: https://useaura.tech
2. Dashboard should load data ✅
3. Analytics should show charts ✅
4. Chatbox should respond ✅

---

## 🐛 Troubleshooting

### Backend not responding:
- Check Render/Railway logs for errors
- Verify all environment variables are set
- Test backend directly: `https://your-backend-url.onrender.com/api/dashboard-data`

### CORS errors:
- Make sure CORS is configured to allow your frontend domain
- Check browser console for specific error messages

### Snowflake connection issues:
- Verify credentials in environment variables
- Check Snowflake account is accessible from Render's IP range
- Test connection in Render logs

---

## 💰 Cost Considerations

**Render Free Tier:**
- ✅ Free for 750 hours/month
- ⚠️ Spins down after 15 minutes of inactivity (cold starts)
- ⚠️ Limited to 512 MB RAM

**Railway Free Tier:**
- ✅ $5 free credit per month
- ✅ No cold starts
- ✅ Better performance

For production, consider upgrading to paid tiers for better reliability.

---

## 🎉 You're Done!

Once backend is deployed and frontend is updated, your full-stack app will be live at https://useaura.tech! 🚀
