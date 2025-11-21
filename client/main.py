import os
import sys
import requests
import time
import pyperclip  # Need to install this: pip install pyperclip

from device_id import get_device_id
from security import encrypt_token, decrypt_token, validate_token

SERVER_URL = "https://ootp-auth-system-hrcayu3wx-ritheshs-projects-2bddf162.vercel.app"
TOKEN_FILE = "token.enc"

import th

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_protected_app(user_id):
    clear_screen()
    print("="*50)
    print(f"WELCOME, {user_id}!")
    print("="*50)
    print("Authentication Successful. Launching App...")
    time.sleep(1)
    
    try:
        th.main()
    except Exception as e:
        print(f"Error running application: {e}")
        input("Press Enter to exit...")

def authenticate():
    # 1. Extract Machine ID
    device_id = get_device_id()
    
    # 2. Check for existing token
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "rb") as f:
                encrypted_data = f.read()
            token = decrypt_token(encrypted_data, device_id)
            claims = validate_token(token, device_id)
            run_protected_app(claims.get("sub"))
            return
        except Exception:
            pass # Invalid token, proceed to auth

    # 3. Registration / Approval Flow
    clear_screen()
    print("="*50)
    print("   DEVICE AUTHORIZATION REQUIRED")
    print("="*50)
    
    user_id = input("Enter your Name/ID: ").strip()
    if not user_id: return

    print(f"\nYour Device ID is:\n{device_id}\n")
    
    try:
        pyperclip.copy(device_id)
        print("(Copied to clipboard!)")
    except:
        pass

    print("\n[-] Registering with server...")
    try:
        requests.post(f"{SERVER_URL}/register_device", json={
            "device_id": device_id,
            "identifier": user_id
        })
    except Exception as e:
        print(f"Error contacting server: {e}")
        input("Press Enter to exit...")
        return

    print("\n[!] STATUS: PENDING APPROVAL")
    print("Please ask the Admin to approve this device.")
    print("Waiting for approval... (Ctrl+C to cancel)")

    # Poll for approval
    while True:
        try:
            resp = requests.get(f"{SERVER_URL}/check_approval", params={"device_id": device_id})
            if resp.status_code == 200:
                data = resp.json()
                if data.get("approved"):
                    print("\n[+] APPROVED! Downloading token...")
                    access_token = data["access_token"]
                    
                    # Validate & Save
                    validate_token(access_token, device_id)
                    encrypted = encrypt_token(access_token, device_id)
                    with open(TOKEN_FILE, "wb") as f:
                        f.write(encrypted)
                        
                    time.sleep(1)
                    run_protected_app(user_id)
                    return
            
            # Wait before polling again
            for i in range(5):
                print(".", end="", flush=True)
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nCancelled.")
            return
        except Exception as e:
            print(f"\nError: {e}")
            time.sleep(5)

if __name__ == "__main__":
    authenticate()
