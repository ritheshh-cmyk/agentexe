# How the Device Approval Flow Works

## Simple Automatic Flow (What You Wanted!)

### 1. User Opens EXE
```
User double-clicks your application EXE
```

### 2. Automatic Hardware ID Extraction
```python
# This happens automatically in the background
device_id = get_device_id()  # Extracts unique hardware ID
```

### 3. Automatic Registration
```python
# Client automatically sends to server
POST /register_device
{
    "device_id": "abc123...",
    "identifier": "User's PC Name"
}
```

### 4. Admin Sees Request
- Admin opens: `https://your-app.vercel.app/admin`
- Sees new device in the table
- Clicks "Approve" button
- Enters admin password

### 5. Client Gets Approved Automatically
```python
# Client polls every few seconds
GET /check_approval?device_id=abc123...

# When approved, receives:
{
    "approved": true,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "expires_in": 86400  # 24 hours
}
```

### 6. Token Saved Locally
```python
# Token encrypted with hardware ID and saved
# File: token.enc
```

### 7. Offline Operation
- Client can now work for 24 hours without internet
- Token verified locally using embedded public key
- After 24 hours, needs re-approval

---

## No Heavy Infrastructure Needed!

✅ **Lightweight** - Just FastAPI + PostgreSQL  
✅ **Serverless** - Runs on Vercel's free tier  
✅ **Automatic** - Everything happens in the background  
✅ **Secure** - JWT tokens, hardware binding, encryption  

---

## What You Need to Do

1. **Create Vercel Postgres database** (see `vercel_setup.md`)
2. **Redeploy** your application
3. **Done!** Everything else is automatic

The client EXE handles everything automatically:
- Extracts hardware ID
- Registers with server
- Polls for approval
- Saves token
- Works offline

No manual steps needed from the end user!
