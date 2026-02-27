# 🚀 Deployment Guide

Complete guide to deploy your Telecom Churn Prediction MLOps project.

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:
- [x] All code is working locally
- [x] Models are trained
- [x] Tests are passing
- [x] Documentation is complete
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Render account created

---

## 🎯 Deployment Options

### Option 1: Streamlit Dashboard (Recommended for Demo)
**Platform**: Streamlit Community Cloud (Free)  
**Best For**: Portfolio, demos, presentations  
**URL**: Custom subdomain (yourapp.streamlit.app)

### Option 2: FastAPI Backend
**Platform**: Render (Free tier)  
**Best For**: API access, production use  
**URL**: Custom subdomain (yourapp.onrender.com)

### Option 3: Both (Full Stack)
Deploy both dashboard and API separately

---

## 🔧 Step 1: Prepare for Deployment

### 1.1 Create GitHub Repository

```bash
# Navigate to project
cd telecom-churn-mlops

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Complete churn prediction MLOps project"

# Create repository on GitHub
# Go to: https://github.com/new
# Repository name: telecom-churn-mlops
# Description: AI-powered customer churn prediction with MLOps and business impact analysis
# Public or Private: Public (for free deployment)
# Don't initialize with README (we have one)

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/telecom-churn-mlops.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 1.2 Verify Files

Ensure these files exist:
- [x] `requirements.txt`
- [x] `app.py` (for Streamlit)
- [x] `Procfile` (for Render API)
- [x] `render.yaml` (for Render)
- [x] `.streamlit/config.toml`
- [x] Models in `models/` directory

---

## 🎨 Option 1: Deploy Streamlit Dashboard

### Step 1: Sign Up for Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "Sign up" or "Get started"
3. Sign in with GitHub
4. Authorize Streamlit to access your repositories

### Step 2: Deploy Your App

1. Click "New app" button
2. Select your repository: `YOUR_USERNAME/telecom-churn-mlops`
3. Branch: `main`
4. Main file path: `app.py`
5. App URL: Choose a custom name (e.g., `churn-prediction-mlops`)

### Step 3: Advanced Settings (Optional)

Click "Advanced settings" and add:

**Python version**: 3.10

**Secrets** (if needed):
```toml
# No secrets needed for this project
```

### Step 4: Deploy

1. Click "Deploy!"
2. Wait 2-5 minutes for deployment
3. Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

### Step 5: Test Deployment

1. Visit your app URL
2. Test single customer prediction
3. Upload a CSV for bulk analysis
4. Verify all features work

### Troubleshooting Streamlit

**Issue**: App crashes on startup
**Solution**: Check logs, ensure all dependencies in requirements.txt

**Issue**: Models not found
**Solution**: Ensure models are committed to git (check .gitignore)

**Issue**: Memory limit exceeded
**Solution**: Streamlit Cloud has 1GB limit, optimize model size

---

## 🔌 Option 2: Deploy FastAPI Backend

### Step 1: Sign Up for Render

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub
4. Authorize Render to access your repositories

### Step 2: Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `telecom-churn-mlops`
4. Configure:
   - **Name**: `churn-prediction-api`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.api:app --host 0.0.0.0 --port $PORT`

### Step 3: Environment Variables

Add these if needed:
```
PYTHON_VERSION=3.10.0
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait 5-10 minutes for first deployment
3. Your API will be live at: `https://churn-prediction-api.onrender.com`

### Step 5: Test API

```bash
# Test root endpoint
curl https://YOUR-APP.onrender.com/

# Test health check
curl https://YOUR-APP.onrender.com/health

# Test prediction (use Postman or curl with JSON)
```

### Troubleshooting Render

**Issue**: Build fails
**Solution**: Check build logs, verify requirements.txt

**Issue**: App crashes
**Solution**: Check logs, ensure models are included

**Issue**: Slow cold starts
**Solution**: Free tier sleeps after inactivity, first request takes 30s

---

## 🎯 Option 3: Deploy Both (Recommended)

### Deploy API on Render
Follow Option 2 above

### Deploy Dashboard on Streamlit
Follow Option 1 above

### Update Dashboard to Use Deployed API

If you want dashboard to call your deployed API:

Edit `app.py`:
```python
# Add at top
API_URL = "https://YOUR-API.onrender.com"

# Use API_URL instead of localhost
```

---

## 📦 Important: Including Models in Deployment

### Option A: Commit Models to Git (Small models <100MB)

```bash
# Remove models from .gitignore
# Edit .gitignore and remove:
# models/*.pkl
# models/*.joblib

# Add models
git add models/best_model.pkl
git add models/feature_engineer.pkl

# Commit
git commit -m "Add trained models for deployment"

# Push
git push
```

### Option B: Download Models on Startup (Large models)

Create `download_models.py`:
```python
import urllib.request
import os

def download_models():
    # Upload models to cloud storage (Google Drive, S3, etc.)
    # Download on app startup
    model_url = "YOUR_MODEL_URL"
    urllib.request.urlretrieve(model_url, "models/best_model.pkl")
```

Add to `app.py` before loading models:
```python
if not os.path.exists('models/best_model.pkl'):
    download_models()
```

### Option C: Train on Deployment (Not Recommended)

Add to build command:
```bash
pip install -r requirements.txt && python train_pipeline.py
```

**Note**: This increases deployment time significantly.

---

## 🔒 Security Considerations

### For Production Deployment:

1. **Add Authentication**
```python
# In app.py
import streamlit_authenticator as stauth

# Add login
authenticator = stauth.Authenticate(...)
name, authentication_status, username = authenticator.login('Login', 'main')
```

2. **Environment Variables**
```python
import os
API_KEY = os.getenv('API_KEY')
```

3. **Rate Limiting**
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

4. **HTTPS Only**
Already handled by Streamlit Cloud and Render

---

## 📊 Post-Deployment

### Update README with Live Links

```markdown
## 🌐 Live Demo

- **Dashboard**: https://YOUR-APP.streamlit.app
- **API**: https://YOUR-API.onrender.com
- **API Docs**: https://YOUR-API.onrender.com/docs
```

### Take Screenshots

1. Dashboard homepage
2. Single prediction results
3. Bulk analysis dashboard
4. API documentation
5. MLflow UI (local)

### Share on LinkedIn

```
🚀 Just deployed my ML project!

Built a production-ready Customer Churn Prediction system with:
✅ MLflow experiment tracking
✅ Business impact dashboard (₹12.6L revenue at risk)
✅ ROI calculator (2,420% return)
✅ FastAPI backend + Streamlit frontend
✅ Deployed and live!

Try it: [YOUR-LINK]
Code: [GITHUB-LINK]

#MachineLearning #MLOps #DataScience #Python
```

---

## 🐛 Common Deployment Issues

### Issue 1: Module Not Found
**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```python
# Add to app.py and api.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
```

### Issue 2: Models Not Loading
**Error**: `FileNotFoundError: models/best_model.pkl`

**Solution**:
- Ensure models are in git
- Check .gitignore doesn't exclude them
- Verify file paths are relative

### Issue 3: Memory Limit
**Error**: `MemoryError` or app crashes

**Solution**:
- Optimize model size
- Use model compression
- Upgrade to paid tier
- Use model quantization

### Issue 4: Slow Performance
**Error**: App is slow

**Solution**:
- Use caching (`@st.cache_resource`)
- Optimize data loading
- Reduce model complexity
- Use CDN for static assets

### Issue 5: Port Issues
**Error**: `Address already in use`

**Solution**:
```python
# Use environment variable
port = int(os.getenv('PORT', 8501))
```

---

## 💰 Cost Considerations

### Free Tiers:

**Streamlit Cloud**:
- 1 private app
- Unlimited public apps
- 1GB RAM
- 1 CPU core
- Community support

**Render**:
- 750 hours/month free
- Sleeps after 15 min inactivity
- 512MB RAM
- Shared CPU
- Cold starts (~30s)

### Paid Tiers (Optional):

**Streamlit Cloud** ($20/month):
- More resources
- Private apps
- Priority support

**Render** ($7/month):
- Always on
- More RAM
- Faster performance

---

## 📈 Monitoring & Maintenance

### Monitor Your App

**Streamlit**:
- Check app logs in dashboard
- Monitor usage stats
- Set up alerts

**Render**:
- View logs in dashboard
- Monitor metrics
- Set up health checks

### Update Your App

```bash
# Make changes locally
git add .
git commit -m "Update: description"
git push

# Auto-deploys on push!
```

### Rollback if Needed

**Streamlit**: Revert commit and push
**Render**: Use "Manual Deploy" with previous commit

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Code works locally
- [ ] Tests pass
- [ ] Models trained
- [ ] Documentation complete
- [ ] .gitignore configured
- [ ] requirements.txt updated

### GitHub
- [ ] Repository created
- [ ] Code pushed
- [ ] README updated
- [ ] License added

### Streamlit Cloud
- [ ] Account created
- [ ] App deployed
- [ ] URL works
- [ ] Features tested
- [ ] Screenshots taken

### Render (Optional)
- [ ] Account created
- [ ] API deployed
- [ ] Endpoints tested
- [ ] Docs accessible

### Post-Deployment
- [ ] README updated with links
- [ ] Screenshots added
- [ ] LinkedIn post created
- [ ] Portfolio updated

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Live demo URL
- ✅ Working API
- ✅ Professional portfolio piece
- ✅ Shareable project
- ✅ Interview showcase

**Your project is now live and ready to impress!** 🚀

---

## 📞 Support

### Resources:
- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Render Docs**: https://render.com/docs
- **GitHub Docs**: https://docs.github.com

### Community:
- Streamlit Forum: https://discuss.streamlit.io
- Render Community: https://community.render.com

---

**Ready to deploy? Let's go! 🚀**
