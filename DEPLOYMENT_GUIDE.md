# 🚀 Streamlit Cloud Deployment Guide

## ⚠️ **Important: SQLite Version Issue**

Streamlit Cloud currently has an older version of SQLite (< 3.35.0) which is incompatible with ChromaDB. This guide provides solutions to deploy your ResourceSuggester AI app successfully.

## 🔧 **Solution 1: Use Cloud-Compatible Version (Recommended)**

### **Step 1: Update Your Repository**

1. **Rename the main file:**
   ```bash
   mv streamlit_app.py streamlit_app_local.py
   mv streamlit_app_cloud.py streamlit_app.py
   ```

2. **Update requirements:**
   ```bash
   mv requirements_streamlit.txt requirements_local.txt
   mv requirements_cloud.txt requirements.txt
   ```

3. **Commit and push changes:**
   ```bash
   git add .
   git commit -m "Add Streamlit Cloud compatible version"
   git push origin main
   ```

### **Step 2: Deploy to Streamlit Cloud**

1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Connect your GitHub repository
3. Set the main file path to: `streamlit_app.py`
4. Deploy!

## 🔧 **Solution 2: Alternative Deployment Platforms**

### **Option A: Railway**
- Supports newer SQLite versions
- Easy deployment from GitHub
- Free tier available

### **Option B: Render**
- Supports custom environments
- Can specify SQLite version
- Free tier available

### **Option C: Heroku**
- Supports newer SQLite versions
- Easy deployment
- Paid service

### **Option D: DigitalOcean App Platform**
- Full control over environment
- Supports all dependencies
- Paid service

## 🔧 **Solution 3: Local Deployment with Public Access**

### **Using ngrok (Free)**

1. **Install ngrok:**
   ```bash
   # Download from https://ngrok.com/
   # Or use Homebrew on Mac:
   brew install ngrok
   ```

2. **Run your local app:**
   ```bash
   streamlit run streamlit_app_local.py
   ```

3. **Create public tunnel:**
   ```bash
   ngrok http 8501
   ```

4. **Share the ngrok URL** (e.g., `https://abc123.ngrok.io`)

### **Using Cloudflare Tunnel (Free)**

1. **Install cloudflared:**
   ```bash
   # Download from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   ```

2. **Create tunnel:**
   ```bash
   cloudflared tunnel --url http://localhost:8501
   ```

## 📁 **File Structure for Deployment**

```
resourcesuggest/
├── streamlit_app.py              # Cloud-compatible version
├── streamlit_app_local.py        # Local version with full features
├── requirements.txt              # Cloud requirements
├── requirements_local.txt        # Local requirements
├── src/
│   └── resourcesuggest/
│       ├── crew.py
│       ├── main.py
│       └── tools/
└── README.md
```

## 🔧 **Environment Variables**

### **For Streamlit Cloud:**
- Set `OPENAI_API_KEY` in Streamlit Cloud dashboard
- No need for local `.env` file

### **For Local Development:**
- Create `.env` file with your API keys
- Keep `.env` in `.gitignore`

## 🐛 **Troubleshooting**

### **Common Issues:**

1. **SQLite Version Error:**
   - Use the cloud-compatible version
   - Or deploy to alternative platforms

2. **Import Errors:**
   - Check file paths in `streamlit_app.py`
   - Ensure all dependencies are in `requirements.txt`

3. **API Key Issues:**
   - Set environment variables in Streamlit Cloud
   - Check API key validity

4. **Memory Issues:**
   - Reduce video limit in YouTube search
   - Optimize agent configurations

## 🚀 **Quick Deployment Commands**

### **For Streamlit Cloud:**
```bash
# Switch to cloud version
mv streamlit_app.py streamlit_app_local.py
mv streamlit_app_cloud.py streamlit_app.py
mv requirements_streamlit.txt requirements_local.txt
mv requirements_cloud.txt requirements.txt

# Commit and push
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### **For Local with Public Access:**
```bash
# Run local version
streamlit run streamlit_app_local.py

# In another terminal, create tunnel
ngrok http 8501
```

## 📊 **Performance Considerations**

### **For Cloud Deployment:**
- Use faster models (`gpt-3.5-turbo`, `gpt-4o-mini`)
- Limit YouTube video searches to 3-5
- Implement caching for repeated searches
- Add progress indicators

### **For Local Deployment:**
- Can use full-featured version
- Better performance with local resources
- Full control over dependencies

## 🎯 **Recommended Approach**

1. **Start with Streamlit Cloud** using the cloud-compatible version
2. **Test thoroughly** with your API keys
3. **If issues persist**, use ngrok for local deployment
4. **For production**, consider Railway or Render

## 📞 **Support**

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify all dependencies are compatible
3. Test locally first
4. Consider alternative deployment platforms

---

**Happy Deploying! 🚀**
