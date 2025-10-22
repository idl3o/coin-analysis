# Quick Start Guide

## 🚀 Deploy to Vercel (Production)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - Crypto Analysis Dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/coin-analysis.git
git push -u origin main
```

### Step 2: Deploy to Vercel
1. Go to [vercel.com/new](https://vercel.com/new)
2. Sign in with GitHub
3. Click "Import" on your repository
4. Click "Deploy" (no configuration needed!)
5. Wait 2-3 minutes ⏳
6. Your app is live! 🎉

**That's it!** Your app will be available at `https://your-project.vercel.app`

---

## 💻 Run Locally (Development)

### First Time Setup

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
npm install
```

### Running the App

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python main.py
```
Backend runs at: `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs at: `http://localhost:3000`

Open `http://localhost:3000` in your browser!

---

## 📁 Project Structure

```
coin-analysis/
├── api/              # Vercel serverless functions
├── backend/          # Backend services
├── frontend/         # React dashboard
├── vercel.json       # Vercel config
└── DEPLOYMENT.md     # Detailed deployment guide
```

---

## 🔧 Common Commands

### Development
```bash
# Start backend
cd backend && python main.py

# Start frontend
cd frontend && npm run dev

# Install backend deps
cd backend && pip install -r requirements.txt

# Install frontend deps
cd frontend && npm install
```

### Deployment
```bash
# Deploy to Vercel (via CLI)
npm install -g vercel
vercel login
vercel --prod

# Build frontend locally
cd frontend && npm run build

# Preview production build
cd frontend && npm run preview
```

### Git
```bash
# Initial commit
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/coin-analysis.git
git push -u origin main

# Update deployment (if connected to Vercel)
git add .
git commit -m "Update: description of changes"
git push
# Vercel auto-deploys!
```

---

## 🎯 Quick Test

After deployment, test these:
1. ✅ Visit your Vercel URL
2. ✅ Select "Bitcoin" from the selector
3. ✅ Change timeframe to "30D"
4. ✅ Check if chart displays
5. ✅ Verify RSI indicator shows a value
6. ✅ Check browser console (F12) for errors

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install

# Clear cache
npm cache clean --force
```

### API calls failing
- Check if backend is running on port 8000
- Verify no other app is using port 8000
- Check browser console for CORS errors

### Vercel deployment fails
- Check build logs in Vercel Dashboard
- Verify `vercel.json` syntax
- Ensure all files are committed to Git

---

## 📚 Documentation

- **README.md** - Project overview and features
- **DEPLOYMENT.md** - Comprehensive deployment guide
- **VERCEL_SETUP_SUMMARY.md** - What was configured for Vercel
- **QUICK_START.md** - This file

---

## 🆘 Need Help?

- Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
- Review [Vercel Docs](https://vercel.com/docs)
- Open an issue on GitHub

---

## ⚡ Pro Tips

1. **Auto-deploy**: Connect GitHub to Vercel for automatic deployments on every push
2. **Preview URLs**: Every pull request gets its own preview URL
3. **Custom Domain**: Add your own domain in Vercel Dashboard → Settings → Domains
4. **Analytics**: Enable Vercel Analytics to track usage
5. **Environment Variables**: Add secrets in Vercel Dashboard → Settings → Environment Variables

---

**Ready to deploy? Let's go! 🚀**
