# 🚀 Deploying Aura to useaura.tech

## Prerequisites
- GitHub account with your repository: https://github.com/RyanRana/hackrufall25
- Domain: useaura.tech (purchased from get.tech)
- Vercel account (free): https://vercel.com

---

## 📋 Deployment Steps

### **Step 1: Push Your Code to GitHub**

Make sure all your latest changes are committed and pushed:

```bash
cd /Users/ryanrana/Desktop/hackrufall25
git add .
git commit -m "Prepare for deployment to useaura.tech"
git push origin main
```

### **Step 2: Deploy to Vercel**

1. **Sign up/Login to Vercel**
   - Go to https://vercel.com
   - Sign in with your GitHub account

2. **Import Your Repository**
   - Click "Add New..." → "Project"
   - Select "Import Git Repository"
   - Choose `RyanRana/hackrufall25`
   - Click "Import"

3. **Configure Build Settings**
   - **Framework Preset**: Select "Vite"
   - **Root Directory**: `aria-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. **Add Environment Variables**
   Click "Environment Variables" and add these (from your `.env` file):
   
   ```
   SNOWFLAKE_USER=your_snowflake_user
   SNOWFLAKE_PASSWORD=your_snowflake_password
   SNOWFLAKE_ACCOUNT=your_snowflake_account
   SNOWFLAKE_WAREHOUSE=your_warehouse_name
   SNOWFLAKE_DATABASE=your_database_name
   SNOWFLAKE_SCHEMA=your_schema_name
   GOOGLE_API_KEY=your_google_api_key
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete (~2-3 minutes)
   - You'll get a URL like: `hackrufall25.vercel.app`

### **Step 3: Connect Your Custom Domain**

1. **In Vercel Dashboard**
   - Go to your project → "Settings" → "Domains"
   - Click "Add Domain"
   - Enter: `useaura.tech`
   - Click "Add"

2. **Configure DNS at get.tech**
   - Log in to your get.tech account
   - Go to Domain Management → DNS Settings
   - Add these records:

   **For Root Domain (useaura.tech):**
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   TTL: 3600
   ```

   **For WWW Subdomain:**
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   TTL: 3600
   ```

3. **Verify Domain**
   - Back in Vercel, click "Verify"
   - DNS propagation can take 5-60 minutes
   - Once verified, your site will be live at https://useaura.tech

---

## 🔧 Alternative: Deploy Backend Separately

If you need the Flask backend to run independently:

### **Option A: Deploy Backend to Render**

1. **Create `render.yaml`** (already in your project)
2. Go to https://render.com
3. Connect your GitHub repo
4. Create a new "Web Service"
5. Set:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python api.py`
   - **Environment**: Add all Snowflake & Google API keys

### **Option B: Deploy Backend to Railway**

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python
5. Add environment variables
6. Deploy

### **Update Frontend API URL**

After deploying backend separately, update the API URL in your frontend:

```javascript
// In Chatbox.jsx, Dashboard.jsx, Analytics.jsx
// Change from:
const response = await axios.get('http://localhost:5001/api/dashboard-data');

// To:
const response = await axios.get('https://your-backend-url.com/api/dashboard-data');
```

---

## 🌐 DNS Configuration Details

### **Get.tech DNS Settings**

Log in to your get.tech control panel and configure:

| Type  | Name | Value                  | TTL  |
|-------|------|------------------------|------|
| A     | @    | 76.76.21.21            | 3600 |
| CNAME | www  | cname.vercel-dns.com   | 3600 |

**Note**: If Vercel provides different IP addresses, use those instead.

---

## ✅ Post-Deployment Checklist

- [ ] Site loads at https://useaura.tech
- [ ] Dashboard displays data correctly
- [ ] Analytics page shows charts
- [ ] Chatbox can send messages
- [ ] CSV upload works
- [ ] All API endpoints respond
- [ ] HTTPS certificate is active (Vercel auto-provides)
- [ ] Mobile responsive design works

---

## 🐛 Troubleshooting

### **Issue: "Cannot connect to backend"**
- Check environment variables are set in Vercel
- Verify Snowflake credentials are correct
- Check CORS settings in `backend/api.py`

### **Issue: "DNS not resolving"**
- Wait 30-60 minutes for DNS propagation
- Use https://dnschecker.org to verify propagation
- Clear your browser cache

### **Issue: "Build failed"**
- Check Node.js version compatibility
- Verify all dependencies are in `package.json`
- Check build logs in Vercel dashboard

### **Issue: "API rate limit exceeded"**
- Google Gemini free tier: 15 requests/minute
- Consider upgrading to paid tier
- Implement request caching

---

## 📊 Monitoring & Analytics

### **Add Google Analytics (Optional)**

1. Get tracking ID from https://analytics.google.com
2. Add to `aria-frontend/index.html`:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` files** - Already in `.gitignore`
2. **Use environment variables** for all secrets
3. **Enable HTTPS** - Vercel provides automatically
4. **Rotate API keys** regularly
5. **Set up Vercel password protection** (Settings → Password Protection)

---

## 📞 Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Get.tech Support**: https://get.tech/support
- **GitHub Repo**: https://github.com/RyanRana/hackrufall25

---

## 🎉 You're Live!

Once deployed, your Aura application will be accessible at:
- **Primary**: https://useaura.tech
- **WWW**: https://www.useaura.tech
- **Vercel**: https://hackrufall25.vercel.app

Share your amazing AI-powered retail analytics platform with the world! 🚀
