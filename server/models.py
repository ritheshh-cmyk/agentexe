from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base
from pydantic import BaseModel
from datetime import datetime

# SQLAlchemy Models
class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, index=True)
    otp_hash = Column(String)
    device_id = Column(String)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))

# Pydantic Schemas
class OTPRequest(BaseModel):
    identifier: str
    device_id: str

class OTPVerify(BaseModel):
    identifier: str
    otp: str
    device_id: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class ValidateRequest(BaseModel):
    token: str
    device_id: str
