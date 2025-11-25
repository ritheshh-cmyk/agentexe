# Quick Start: Create Vercel Postgres Database

## ✅ What's Already Done
- ✅ Code updated to support Vercel Postgres
- ✅ Changes committed and pushed to GitHub
- ✅ Vercel will auto-deploy from GitHub

## 🎯 What You Need to Do Now

### Step 1: Log in to Vercel
1. Go to: https://vercel.com/dashboard
2. Log in with your account

### Step 2: Find Your Project
1. You should see your project in the dashboard
2. Click on your project name (likely "otpvalidation" or "agentexe")

### Step 3: Create Postgres Database
1. Click on the **"Storage"** tab (top navigation)
2. Click **"Create Database"** button
3. Select **"Postgres"**
4. Enter database name: `device-approval-db` (or any name you like)
5. Select region: Choose closest to your users (e.g., `Washington, D.C., USA (iad1)`)
6. Click **"Create"** button

### Step 4: Connect Database to Project
1. After database is created, click **"Connect Project"**
2. Select your project from the dropdown
3. Click **"Connect"**
4. Vercel will automatically add environment variables to your project

### Step 5: Verify Deployment
1. Go to **"Deployments"** tab
2. Wait for the latest deployment to finish (should auto-deploy from your git push)
3. Click on the deployment URL when ready

### Step 6: Test It Works!

**Test 1: Health Check**
- Visit: `https://your-deployment-url.vercel.app/health`
- Should show: `{"status": "healthy", "database": "connected"}`

**Test 2: Admin Panel**
- Visit: `https://your-deployment-url.vercel.app/admin`
- Should show empty table (no devices yet)

**Test 3: Register a Device**
- Run your client EXE
- It will automatically register
- Refresh admin panel - you should see the device!

**Test 4: Approve Device**
- Click "Approve" button
- Enter password: `admin123`
- Device gets approved
- Client receives token automatically

---

## 🎉 That's It!

Your device approval system is now fully working on Vercel with persistent storage!

## 📝 Optional: Change Admin Password

For security, set a custom admin password:

1. In Vercel dashboard → Your Project
2. Click **"Settings"** → **"Environment Variables"**
3. Add new variable:
   - Name: `ADMIN_PASSWORD`
   - Value: Your secure password
4. Click **"Save"**
5. Redeploy (or it will auto-deploy)

---

## 🆘 Troubleshooting

**Database not connecting?**
- Make sure you clicked "Connect Project" after creating the database
- Check environment variables are set (Settings → Environment Variables)
- Should see: `POSTGRES_URL`, `POSTGRES_PRISMA_URL`, etc.

**Devices not showing in admin panel?**
- Clear browser cache
- Check `/health` endpoint shows "database: connected"
- Make sure client is pointing to correct server URL

**Need help?**
- Check Vercel logs: `vercel logs --follow`
- Or in dashboard: Deployments → Click deployment → Runtime Logs
