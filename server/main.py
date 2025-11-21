from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
import string

from . import models, database, auth

app = FastAPI(title="OTP Offline Auth System")

# Create tables
models.Base.metadata.create_all(bind=database.engine)

def generate_otp(length=6):
    return ''.join(secrets.choice(string.digits) for _ in range(length))

@app.post("/create_otp", status_code=status.HTTP_201_CREATED)
def create_otp(request: models.OTPRequest, db: Session = Depends(database.get_db)):
    # Generate OTP
    otp_code = generate_otp()
    otp_hash = auth.get_password_hash(otp_code)
    
    # Set expiration (e.g., 5 minutes)
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # Save to DB
    db_otp = models.OTP(
        identifier=request.identifier,
        otp_hash=otp_hash,
        device_id=request.device_id,
        expires_at=expires_at
    )
    db.add(db_otp)
    db.commit()
    db.refresh(db_otp)
    
    # In a real system, send this via Email/SMS. 
    # For this demo, we return it so the user can copy-paste it.
    return {"message": "OTP created", "otp": otp_code} 

@app.post("/verify_otp", response_model=models.TokenResponse)
def verify_otp(request: models.OTPVerify, db: Session = Depends(database.get_db)):
    # Find valid OTP
    # We look for the latest unused OTP for this user/device that hasn't expired
    otp_record = db.query(models.OTP).filter(
        models.OTP.identifier == request.identifier,
        models.OTP.device_id == request.device_id,
        models.OTP.is_used == False,
        models.OTP.expires_at > datetime.utcnow()
    ).order_by(models.OTP.created_at.desc()).first()
    
    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    if not auth.verify_password(request.otp, otp_record.otp_hash):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Mark as used
    otp_record.is_used = True
    db.commit()
    
    # Issue JWT
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, expire_time = auth.create_access_token(
        data={"sub": request.identifier, "device": request.device_id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds())
    }

@app.get("/public_key")
def get_public_key():
    with open("server/public_key.pem", "r") as f:
        return {"public_key": f.read()}
