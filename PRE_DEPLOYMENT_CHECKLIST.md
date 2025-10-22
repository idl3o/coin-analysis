# Pre-Deployment Checklist

Before deploying to Vercel, make sure you've completed these items:

## ✅ Code Preparation

### Backend
- [ ] All backend services work locally
- [ ] `backend/requirements.txt` includes all dependencies
- [ ] `api/requirements.txt` includes all dependencies
- [ ] API endpoints respond correctly
- [ ] No hardcoded secrets or API keys in code
- [ ] CORS is properly configured

### Frontend
- [ ] Frontend runs locally without errors
- [ ] All components render correctly
- [ ] Charts display data properly
- [ ] Technical indicators calculate correctly
- [ ] No console errors in browser
- [ ] API calls work in development
- [ ] Environment variables are set up (`.env` files)

## ✅ Configuration Files

- [ ] `vercel.json` exists in root directory
- [ ] `package.json` exists in root directory
- [ ] `frontend/.env.production` exists
- [ ] `frontend/.env.development` exists
- [ ] `.gitignore` includes sensitive files
- [ ] `.vercelignore` is configured

## ✅ Git Repository

- [ ] Git repository initialized (`git init`)
- [ ] All files are committed
- [ ] Repository pushed to GitHub/GitLab/Bitbucket
- [ ] Repository is public or Vercel has access
- [ ] No sensitive data in git history

## ✅ Vercel Account

- [ ] Vercel account created (free tier is fine)
- [ ] GitHub account connected to Vercel
- [ ] Email verified

## ✅ File Structure

```
✓ coin-analysis/
  ✓ vercel.json
  ✓ package.json
  ✓ .gitignore
  ✓ .vercelignore
  ✓ api/
    ✓ index.py
    ✓ requirements.txt
  ✓ backend/
    ✓ main.py
    ✓ requirements.txt
    ✓ services/
  ✓ frontend/
    ✓ package.json
    ✓ .env.production
    ✓ .env.development
    ✓ src/
```

## ✅ Testing

### Local Testing
- [ ] Backend runs: `cd backend && python main.py`
- [ ] Frontend runs: `cd frontend && npm run dev`
- [ ] Can select different cryptocurrencies
- [ ] Charts update when changing timeframe
- [ ] Technical indicators display correctly
- [ ] Price data loads from CoinGecko
- [ ] No errors in terminal or browser console

### Build Testing
- [ ] Frontend builds successfully: `cd frontend && npm run build`
- [ ] No build errors or warnings
- [ ] Build output is in `frontend/dist/`
- [ ] Preview build works: `npm run preview`

## ✅ API Endpoints

Test all endpoints locally:
- [ ] `GET http://localhost:8000/api/crypto/price/BTC`
- [ ] `GET http://localhost:8000/api/crypto/prices?symbols=BTC,ETH`
- [ ] `GET http://localhost:8000/api/crypto/historical/BTC?days=30`
- [ ] `GET http://localhost:8000/api/crypto/indicators/BTC?days=30`
- [ ] `GET http://localhost:8000/api/crypto/top?limit=10`

## ✅ Dependencies

### Backend Python Packages
- [ ] fastapi
- [ ] mangum (for Vercel serverless)
- [ ] pandas
- [ ] pandas-ta
- [ ] aiohttp
- [ ] requests
- [ ] pydantic

### Frontend NPM Packages
- [ ] react
- [ ] react-dom
- [ ] vite
- [ ] recharts
- [ ] axios
- [ ] lucide-react

## ✅ Environment Variables

- [ ] `VITE_API_BASE_URL` configured in `.env.production` as `/api`
- [ ] `VITE_API_BASE_URL` configured in `.env.development` as `http://localhost:8000/api`
- [ ] No secrets committed to git

## ✅ Documentation

- [ ] README.md is up to date
- [ ] DEPLOYMENT.md exists
- [ ] API endpoints are documented
- [ ] Installation instructions are clear

## ✅ Final Checks

- [ ] Project name decided (for Vercel URL)
- [ ] No merge conflicts
- [ ] Latest code is pushed to main branch
- [ ] All TODOs are resolved or documented

## 🚀 Ready to Deploy!

If all items are checked, you're ready to deploy:

### Option 1: Vercel Dashboard
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your repository
3. Click "Deploy"

### Option 2: Vercel CLI
```bash
npm install -g vercel
vercel login
vercel --prod
```

---

## 🎯 Post-Deployment Checklist

After deploying, verify:

- [ ] Deployment succeeded (no errors)
- [ ] Site loads at Vercel URL
- [ ] Frontend displays correctly
- [ ] Can select cryptocurrencies
- [ ] Charts render with data
- [ ] Technical indicators calculate
- [ ] No console errors (F12)
- [ ] No CORS errors
- [ ] API responses are fast (<2 seconds)
- [ ] Mobile view works correctly

---

## 📊 Success Criteria

Your deployment is successful when:

1. ✅ **Homepage loads** - No blank screens
2. ✅ **Crypto selector works** - Can click different coins
3. ✅ **Chart displays data** - Shows price history
4. ✅ **Indicators calculate** - RSI, MACD, etc. show values
5. ✅ **Timeframes work** - Can switch between 7D, 30D, 90D, 180D
6. ✅ **No errors** - Console is clean
7. ✅ **Responsive** - Works on mobile and desktop
8. ✅ **Fast loading** - Under 3 seconds initial load

---

## 🐛 Common Issues

### If you see errors:

**"Cannot GET /api/crypto/..."**
- Check `vercel.json` routes configuration
- Verify `api/index.py` exists

**"CORS error"**
- Check CORS configuration in `api/index.py`
- Ensure `allow_origins=["*"]` is set

**"Module not found"**
- Check `api/requirements.txt` has all dependencies
- Redeploy after updating requirements.txt

**"Build failed"**
- Check build logs in Vercel Dashboard
- Verify `frontend/package.json` scripts are correct

---

## 📞 Support

If you encounter issues:
1. Check [DEPLOYMENT.md](DEPLOYMENT.md)
2. Review [Vercel Docs](https://vercel.com/docs)
3. Check [Vercel Community](https://github.com/vercel/vercel/discussions)

---

**Everything checked? Great! You're ready to deploy! 🚀**

```bash
git push origin main
# Then import to Vercel and deploy!
```
