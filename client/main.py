import os
import sys
import requests
import time
from getpass import getpass

from device_id import get_device_id
from security import encrypt_token, decrypt_token, validate_token

SERVER_URL = "http://127.0.0.1:8000"
TOKEN_FILE = "token.enc"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

import th

def run_protected_app(user_id):
    clear_screen()
    print("="*50)
    print(f"WELCOME, {user_id}!")
    print("="*50)
    print("Authentication Successful. Launching App...")
    time.sleep(1)
    
    # Launch the protected application
    try:
        th.main()
    except Exception as e:
        print(f"Error running application: {e}")
        input("Press Enter to exit...")


def authenticate():
    device_id = get_device_id()
    print(f"Device ID: {device_id}")
    
    # 1. Check for existing token
    if os.path.exists(TOKEN_FILE):
        try:
            print("Found existing token. Validating...")
            with open(TOKEN_FILE, "rb") as f:
                encrypted_data = f.read()
            
            token = decrypt_token(encrypted_data, device_id)
            claims = validate_token(token, device_id)
            
            print("Token is valid!")
            time.sleep(1)
            run_protected_app(claims.get("sub"))
            return
        except Exception as e:
            print(f"Token validation failed: {e}")
            print("Re-authentication required.")
            try:
                os.remove(TOKEN_FILE)
            except:
                pass
            time.sleep(2)
            clear_screen()

    # 2. Start Auth Flow
    print("--- AUTHENTICATION REQUIRED ---")
    user_id = input("Enter User ID: ").strip()
    if not user_id:
        print("User ID cannot be empty.")
        return

    # Request OTP
    try:
        print(f"Requesting OTP from {SERVER_URL}...")
        resp = requests.post(f"{SERVER_URL}/create_otp", json={
            "identifier": user_id,
            "device_id": device_id
        })
        resp.raise_for_status()
        data = resp.json()
        
        # In a real app, you wouldn't print this. 
        # But for this demo/MVP where we don't have email setup:
        print(f"\n[DEMO MODE] Your OTP is: {data.get('otp')}\n")
        
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return

    # Verify OTP
    otp_input = input("Enter OTP: ").strip()
    
    try:
        print("Verifying...")
        resp = requests.post(f"{SERVER_URL}/verify_otp", json={
            "identifier": user_id,
            "otp": otp_input,
            "device_id": device_id
        })
        resp.raise_for_status()
        token_data = resp.json()
        access_token = token_data["access_token"]
        
        # Validate immediately to be sure
        validate_token(access_token, device_id)
        
        # Save encrypted
        encrypted = encrypt_token(access_token, device_id)
        with open(TOKEN_FILE, "wb") as f:
            f.write(encrypted)
            
        print("Authentication successful! Token saved.")
        time.sleep(1)
        run_protected_app(user_id)
        
    except Exception as e:
        print(f"Authentication failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Server message: {e.response.text}")

if __name__ == "__main__":
    try:
        authenticate()
    except KeyboardInterrupt:
        print("\nExiting...")
