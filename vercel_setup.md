# Vercel Postgres Setup Guide

This guide will help you set up Vercel Postgres for your device approval system so that device registrations persist properly.

## Why You Need This

Your current deployment uses in-memory SQLite which **loses all data** when Vercel's serverless functions restart. This causes:
- ❌ Device registrations disappear
- ❌ Admin panel shows no devices
- ❌ Users can't get approved

Vercel Postgres fixes this by providing **persistent storage**.

---

## Step-by-Step Setup

### 1. Create Vercel Postgres Database

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Select your project (otpvalidation)
3. Click on the **"Storage"** tab
4. Click **"Create Database"**
5. Select **"Postgres"**
6. Choose a database name (e.g., `device-approval-db`)
7. Select a region (choose one close to your users)
8. Click **"Create"**

### 2. Connect Database to Your Project

Vercel will automatically:
- ✅ Create the database
- ✅ Set environment variables (`POSTGRES_URL`, `POSTGRES_PRISMA_URL`, etc.)
- ✅ Make them available to your deployment

**No manual configuration needed!** The environment variables are automatically injected.

### 3. Redeploy Your Application

After creating the database, you need to redeploy:

**Option A: Push to Git (Recommended)**
```bash
git add .
git commit -m "Add Vercel Postgres support"
git push
```

**Option B: Manual Deploy via Vercel CLI**
```bash
vercel --prod
```

**Option C: Redeploy from Dashboard**
1. Go to your project in Vercel dashboard
2. Click "Deployments" tab
3. Click the three dots (...) on the latest deployment
4. Click "Redeploy"

### 4. Verify It Works

After deployment completes:

1. **Test the health endpoint:**
   - Visit: `https://your-app.vercel.app/health`
   - Should show: `{"status": "healthy", "database": "connected"}`

2. **Run your client EXE:**
   - It will register the device
   - Device ID will be sent to the database

3. **Check the admin panel:**
   - Visit: `https://your-app.vercel.app/admin`
   - You should now see your registered device!

4. **Approve the device:**
   - Click "Approve" button
   - Enter admin password (default: `admin123`)
   - Device gets approved

5. **Client receives token:**
   - Client will automatically check approval status
   - Receives 24-hour token
   - Can now work offline!

---

## Environment Variables

Vercel Postgres automatically sets these variables:

- `POSTGRES_URL` - Full connection string (used by your app)
- `POSTGRES_PRISMA_URL` - Connection pooling URL
- `POSTGRES_URL_NON_POOLING` - Direct connection
- `POSTGRES_USER` - Database username
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DATABASE` - Database name
- `POSTGRES_HOST` - Database host

Your code uses `POSTGRES_URL` automatically (see `server/database.py`).

---

## Optional: Set Admin Password

For security, change the default admin password:

1. In Vercel dashboard, go to your project
2. Click **"Settings"** → **"Environment Variables"**
3. Add new variable:
   - **Name:** `ADMIN_PASSWORD`
   - **Value:** Your secure password
   - **Environment:** Production
4. Click **"Save"**
5. Redeploy the application

---

## Troubleshooting

### Database connection fails
- Check the `/health` endpoint
- Verify database is in the same region as your deployment
- Check Vercel logs: `vercel logs --follow`

### Devices still not showing
- Clear browser cache and refresh admin panel
- Check database was created successfully in Storage tab
- Verify environment variables are set (Settings → Environment Variables)

### "No module named 'psycopg2'" error
- Make sure `psycopg2-binary` is in `requirements.txt`
- Redeploy the application

---

## Local Development

For local testing, the app will use SQLite automatically:

```bash
cd server
uvicorn main:app --reload
```

To test with Postgres locally:
1. Get the `POSTGRES_URL` from Vercel dashboard (Settings → Environment Variables)
2. Set it in your terminal:
   ```bash
   # Windows PowerShell
   $env:POSTGRES_URL="your-postgres-url-here"
   
   # Windows CMD
   set POSTGRES_URL=your-postgres-url-here
   
   # Linux/Mac
   export POSTGRES_URL="your-postgres-url-here"
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

---

## What Changed in Your Code

✅ **database.py** - Now uses `POSTGRES_URL` environment variable
✅ **Connection pooling** - Optimized for serverless (NullPool)
✅ **SSL support** - Required for Vercel Postgres
✅ **Fallback** - Still uses SQLite for local development

No changes needed to your client code!

---

## Next Steps

1. ✅ Create Vercel Postgres database
2. ✅ Redeploy your application
3. ✅ Test device registration
4. ✅ Verify admin panel shows devices
5. ✅ (Optional) Set custom admin password

Your device approval system will now work reliably on Vercel! 🎉
