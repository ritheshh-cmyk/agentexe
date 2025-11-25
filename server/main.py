from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os

# Local imports
from . import models, database, auth

app = FastAPI(title="Device Approval Auth System")

# Admin password (set via env var in Vercel)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")



@app.post("/register_device")
def register_device(request: models.DeviceRegister, db: Session = Depends(database.get_db)):
    # Check if exists
    db_device = db.query(models.Device).filter(models.Device.device_id == request.device_id).first()
    if not db_device:
        db_device = models.Device(
            device_id=request.device_id, 
            identifier=request.identifier,
            approved=False # Default to False, requires Admin approval
        )
        db.add(db_device)
        db.commit()
    return {"message": "Device registered", "approved": db_device.approved}

@app.get("/check_approval")
def check_approval(device_id: str, db: Session = Depends(database.get_db)):
    db_device = db.query(models.Device).filter(models.Device.device_id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if not db_device.approved:
        return {"approved": False}
    
    # If approved, issue token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, expire_time = auth.create_access_token(
        data={"sub": db_device.identifier, "device": device_id},
        expires_delta=access_token_expires
    )
    
    return {
        "approved": True,
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds())
    }

@app.post("/approve_device")
def approve_device(request: models.DeviceApproval, db: Session = Depends(database.get_db)):
    if request.admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Invalid admin password")
        
    db_device = db.query(models.Device).filter(models.Device.device_id == request.device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
        
    db_device.approved = request.approved
    db.commit()
    return {"message": f"Device {'approved' if request.approved else 'rejected'}"}

@app.get("/")
def root():
    return {"message": "Device Approval System is Running", "docs": "/docs"}

@app.get("/health")
def health_check():
    try:
        # Test database connection
        db = next(database.get_db())
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "type": type(e).__name__}

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(db: Session = Depends(database.get_db)):
    try:
        devices = db.query(models.Device).all()
    except Exception as e:
        return f"<h1>Error Connecting to Database</h1><p>{str(e)}</p>"

    
    rows = ""
    for d in devices:
        status_color = "green" if d.approved else "red"
        status_text = "Approved" if d.approved else "Pending"
        action = "Reject" if d.approved else "Approve"
        new_state = "false" if d.approved else "true"
        
        rows += f"""
        <tr>
            <td>{d.identifier}</td>
            <td>{d.device_id}</td>
            <td style="color:{status_color}">{status_text}</td>
            <td>{d.created_at}</td>
            <td>
                <button onclick="approve('{d.device_id}', {new_state})">{action}</button>
            </td>
        </tr>
        """
        
    html = f"""
    <html>
    <head>
        <title>Admin Dashboard</title>
        <style>
            body {{ font-family: sans-serif; padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            button {{ padding: 5px 10px; cursor: pointer; }}
        </style>
        <script>
            async function approve(deviceId, state) {{
                const password = prompt("Enter Admin Password:");
                if (!password) return;
                
                const res = await fetch('/approve_device', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ device_id: deviceId, approved: state, admin_password: password }})
                }});
                
                if (res.ok) {{
                    location.reload();
                }} else {{
                    alert("Error: " + (await res.json()).detail);
                }}
            }}
        </script>
    </head>
    <body>
        <h1>Device Approval Dashboard</h1>
        <table>
            <tr>
                <th>User ID</th>
                <th>Device ID</th>
                <th>Status</th>
                <th>Created At</th>
                <th>Action</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return html

# Fix path resolution for Vercel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "private_key.pem")
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "public_key.pem")

@app.get("/public_key")
def get_public_key():
    with open(PUBLIC_KEY_PATH, "r") as f:
        return {"public_key": f.read()}

