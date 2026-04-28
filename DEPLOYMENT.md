# PL Pulse Deployment Guide

This guide provides instructions for deploying PL Pulse to various hosting platforms.

## Quick Deploy Options

### Option 1: Render (Recommended - Free Tier Available)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Steps:**
1. Fork the repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml`
6. Click "Create Web Service"
7. Wait for deployment to complete (~5 minutes)

**Free Tier Limitations:**
- Service spins down after 15 minutes of inactivity
- Spins up on first request (may take 30-60 seconds)
- 750 hours/month free

### Option 2: Railway (Easy Deploy)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

**Steps:**
1. Click the "Deploy on Railway" button above
2. Connect your GitHub account
3. Select the `pl-pulse` repository
4. Railway will automatically detect `railway.json`
5. Click "Deploy"
6. Wait for deployment (~3-5 minutes)

**Free Tier:**
- $5 credit per month
- Persistent service (doesn't spin down)
- Custom domain support

### Option 3: Heroku

**Steps:**
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to Heroku:
   ```bash
   heroku login
   ```
3. Create a new app:
   ```bash
   cd pl-pulse
   heroku create pl-pulse-app
   ```
4. Deploy:
   ```bash
   git push heroku main
   ```
5. Open your app:
   ```bash
   heroku open
   ```

**Note:** Heroku no longer offers a free tier. Eco plan starts at $5/month.

### Option 4: Docker (Self-Hosted)

**Build and Run Locally:**
```bash
# Build image
docker build -t pl-pulse .

# Run container
docker run -p 8000:8000 pl-pulse
```

**Deploy to any Docker-compatible platform:**
- Google Cloud Run
- AWS ECS
- Azure Container Instances
- DigitalOcean App Platform
- Fly.io

### Option 5: Vercel (Serverless)

**Note:** Vercel is optimized for Next.js. For FastAPI, you'll need to use serverless functions.

**Steps:**
1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```
2. Deploy:
   ```bash
   cd pl-pulse
   vercel
   ```

## Environment Variables

Set these environment variables in your hosting platform:

```
DATABASE_URL=sqlite:///./plpulse.db
SECRET_KEY=your-random-secret-key-here
DEBUG=false
LOG_LEVEL=INFO
SCRAPE_RATE_LIMIT=2.0
USER_AGENT=PLPulse/1.0 (contact@plpulse.com)
```

## Database Setup

### SQLite (Default - Good for Free Tiers)
- Already configured
- Data persists in `plpulse.db` file
- Automatic seeding on first run

### PostgreSQL (Production Recommended)

**Render:**
- Add PostgreSQL database in Render dashboard
- Copy connection string to `DATABASE_URL`

**Railway:**
- Add PostgreSQL plugin
- Railway auto-configures `DATABASE_URL`

**Heroku:**
```bash
heroku addons:create heroku-postgresql:mini
```

**Update `app/config.py` for PostgreSQL:**
```python
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./plpulse.db")
# Fix for Heroku postgres:// → postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
```

## Post-Deployment Steps

1. **Verify Deployment:**
   ```bash
   curl https://your-app-url.com/health
   ```

2. **Seed Database (if needed):**
   ```bash
   # For Heroku
   heroku run python scripts/seed_database.py
   
   # For Railway/Render - runs automatically
   ```

3. **Check Logs:**
   ```bash
   # Heroku
   heroku logs --tail
   
   # Railway
   railway logs
   
   # Render - view in dashboard
   ```

4. **Test Endpoints:**
   - Visit `https://your-app-url.com/`
   - Check API docs at `https://your-app-url.com/docs`
   - Test `/api/teams/`, `/api/standings/`, etc.

## Custom Domain

### Render:
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records as instructed

### Railway:
1. Go to Settings → Domains
2. Add custom domain
3. Configure DNS

### Heroku:
```bash
heroku domains:add www.yourdomain.com
```

## Performance Optimization

### Enable Caching
Add Redis for production:
```bash
# Heroku
heroku addons:create heroku-redis:mini

# Railway
# Add Redis plugin from dashboard
```

### Use CDN for Static Files
- Upload static files to Cloudflare, AWS S3, or similar
- Update static file paths in templates

### Database Connection Pooling
Update `app/core/database.py`:
```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)
```

## Monitoring

### Health Checks
All platforms support health check endpoints:
- Endpoint: `/health`
- Expected response: `{"status":"healthy","version":"1.0.0"}`

### Logging
- Logs are automatically captured by hosting platforms
- View in respective dashboards

### Uptime Monitoring
Use free services:
- [UptimeRobot](https://uptimerobot.com/)
- [Pingdom](https://www.pingdom.com/)
- [Better Uptime](https://betteruptime.com/)

## Troubleshooting

### App Won't Start
1. Check logs for errors
2. Verify all environment variables are set
3. Ensure `requirements.txt` is up to date
4. Check Python version compatibility

### Database Errors
1. Verify `DATABASE_URL` is correct
2. Check database connection from logs
3. Ensure migrations are applied
4. Re-run seed script if needed

### Static Files Not Loading
1. Check file paths in templates
2. Verify static files are included in deployment
3. Check `.dockerignore` and `.gitignore`

### Slow Performance
1. Check if using free tier (cold starts)
2. Enable caching
3. Optimize database queries
4. Consider upgrading to paid tier

## Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Render** | 750 hrs/mo | $7/mo | Easy deployment |
| **Railway** | $5 credit/mo | $5/mo + usage | Persistent apps |
| **Heroku** | None | $5/mo (Eco) | Enterprise ready |
| **Fly.io** | Limited | $1.94/mo | Global edge |
| **Vercel** | Generous | $20/mo | Serverless |

## Recommended Setup

**For Development/Testing:**
- Render Free Tier
- SQLite database
- No custom domain

**For Production:**
- Railway or Render Paid
- PostgreSQL database
- Custom domain
- Redis caching
- Uptime monitoring

## Support

For deployment issues:
- Check platform-specific documentation
- Review application logs
- Open an issue on GitHub
- Contact platform support

---

**Quick Start:** For the fastest deployment, use Render's one-click deploy with the button at the top of this guide!
