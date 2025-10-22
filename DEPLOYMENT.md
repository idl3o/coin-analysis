# Deploying to Vercel

This guide will walk you through deploying your Crypto Analysis Dashboard to Vercel.

## Prerequisites

- A [Vercel account](https://vercel.com/signup) (free tier works great!)
- Git installed on your machine
- Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Project Structure for Vercel

The project has been configured for Vercel deployment with the following structure:

```
coin-analysis/
├── vercel.json          # Vercel configuration
├── package.json         # Root package.json for build commands
├── api/                 # Backend (Serverless Functions)
│   ├── index.py        # Main API handler
│   └── requirements.txt # Python dependencies
├── backend/            # Backend services (imported by api/)
│   └── services/
└── frontend/           # React frontend
    ├── package.json
    └── src/
```

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Crypto Analysis Dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/coin-analysis.git
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration

3. **Configure Build Settings** (should be auto-detected)
   - Framework Preset: `Other`
   - Build Command: `npm run vercel-build`
   - Output Directory: `frontend/dist`
   - Install Command: `npm install`

4. **Deploy**
   - Click "Deploy"
   - Wait for the deployment to complete (2-3 minutes)
   - Your app will be live at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy? `Y`
   - Which scope? Choose your account
   - Link to existing project? `N`
   - Project name: `crypto-analysis` (or your preferred name)
   - In which directory is your code located? `./`

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Configuration Files Explained

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": { "distDir": "frontend/dist" }
    },
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.py" },
    { "src": "/(.*)", "dest": "/frontend/$1" }
  ]
}
```

This configures:
- **Frontend**: Built as static site from `frontend/`
- **Backend**: Python serverless functions from `api/`
- **Routing**: API calls to `/api/*` → Python backend, everything else → React frontend

### Environment Variables

The app uses different API URLs for development and production:

- **Development**: `http://localhost:8000/api`
- **Production**: `/api` (relative path, same domain)

These are configured in:
- `frontend/.env.development`
- `frontend/.env.production`

## Post-Deployment

### 1. Test Your Deployment

Visit your Vercel URL and test:
- ✅ Frontend loads correctly
- ✅ Can select cryptocurrencies
- ✅ Charts display data
- ✅ Technical indicators load
- ✅ No CORS errors in console

### 2. Custom Domain (Optional)

1. Go to your project in Vercel Dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

### 3. Monitor Performance

- Check the "Analytics" tab in Vercel Dashboard
- Monitor API response times
- Review error logs if issues occur

## Troubleshooting

### Issue: API calls failing (500 errors)

**Solution**: Check the Function logs in Vercel Dashboard
- Go to Deployments → Select deployment → Functions tab
- Look for Python errors
- Common issues:
  - Missing dependencies in `api/requirements.txt`
  - Import path issues
  - CoinGecko API rate limiting

### Issue: Frontend shows "Cannot GET /api/..."

**Solution**: Ensure `vercel.json` routes are correct
```json
{
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.py" }
  ]
}
```

### Issue: Build fails with Python errors

**Solution**:
1. Ensure Python 3.9 is specified in `vercel.json`
2. Check all dependencies are in `api/requirements.txt`
3. Verify imports work with the new structure

### Issue: CORS errors

**Solution**: The API is configured with `allow_origins=["*"]` which should work. If issues persist:
1. Check browser console for exact error
2. Verify the API URL in frontend matches deployment URL
3. Ensure `VITE_API_BASE_URL` environment variable is set correctly

### Issue: CoinGecko API Rate Limiting

**Solution**: CoinGecko free tier has rate limits:
- 10-30 calls/minute
- Add delays between requests if needed
- Consider upgrading to CoinGecko Pro API for production

## Performance Optimization

### 1. Enable Edge Caching

Add to `vercel.json`:
```json
{
  "headers": [
    {
      "source": "/api/crypto/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=60, stale-while-revalidate"
        }
      ]
    }
  ]
}
```

### 2. Optimize Bundle Size

```bash
cd frontend
npm run build
# Check the build output for bundle sizes
```

### 3. Add Loading States

Already implemented in the Dashboard component!

## Continuous Deployment

Once connected to GitHub, Vercel automatically:
- ✅ Deploys every push to `main` branch
- ✅ Creates preview deployments for pull requests
- ✅ Runs build checks before merging

## Environment Variables in Vercel

If you need to add environment variables:

1. Go to Project Settings → Environment Variables
2. Add variables:
   - `VITE_API_BASE_URL` → `/api` (for production)
3. Redeploy for changes to take effect

## Monitoring & Analytics

### Built-in Vercel Analytics
- Page views
- API function invocations
- Performance metrics
- Geographic distribution

### Custom Monitoring
Consider adding:
- [Sentry](https://sentry.io) for error tracking
- [LogRocket](https://logrocket.com) for session replay
- Google Analytics for user tracking

## Limits & Quotas (Free Tier)

Vercel Free Tier includes:
- ✅ 100 GB bandwidth/month
- ✅ 100 GB-hours serverless function execution
- ✅ 6,000 build minutes/month
- ✅ Unlimited API requests

Perfect for this project! 🚀

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- [Project Issues](https://github.com/YOUR_USERNAME/coin-analysis/issues)

## Quick Reference Commands

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs [deployment-url]

# List deployments
vercel ls

# Remove deployment
vercel rm [deployment-url]
```

---

🎉 **Congratulations!** Your Crypto Analysis Dashboard is now live on Vercel!

Share your deployment URL and start analyzing cryptocurrencies! 📈
