import base64
import hashlib
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from jose import jwt, JWTError
from datetime import datetime

def get_public_key():
    # In a real PyInstaller build, you might bundle this as a resource
    # For now we assume it's in the same directory or passed in
    path = os.path.join(os.path.dirname(__file__), "public_key.pem")
    if not os.path.exists(path):
        # Fallback for development if running from root
        path = "client/public_key.pem"
        
    with open(path, "rb") as f:
        return f.read()

def derive_key(device_id: str) -> bytes:
    """
    Derive a Fernet key from the device ID.
    We use a static salt because the device ID itself is the secret here 
    (binding to the machine).
    """
    salt = b"static_salt_for_device_binding" 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(device_id.encode()))
    return key

def encrypt_token(token: str, device_id: str) -> bytes:
    key = derive_key(device_id)
    f = Fernet(key)
    return f.encrypt(token.encode())

def decrypt_token(encrypted_token: bytes, device_id: str) -> str:
    key = derive_key(device_id)
    f = Fernet(key)
    return f.decrypt(encrypted_token).decode()

def validate_token(token: str, device_id: str):
    """
    Validates the JWT offline using the public key.
    Returns decoded claims if valid, raises Exception if not.
    """
    public_key = get_public_key()
    
    try:
        # Verify signature and standard claims (exp)
        # We also verify that the 'device' claim matches the current device_id
        claims = jwt.decode(
            token, 
            public_key, 
            algorithms=["RS256"],
            options={"verify_aud": False} # We use custom device claim
        )
        
        # Custom device check
        if claims.get("device") != device_id:
            raise Exception("Token is not bound to this device")
            
        # Check expiration manually just to be sure (jwt lib does it too)
        exp = claims.get("exp")
        if datetime.utcnow().timestamp() > exp:
             raise Exception("Token expired")
             
        return claims
        
    except JWTError as e:
        raise Exception(f"Token validation failed: {str(e)}")
