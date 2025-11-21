# OTP Offline Authentication System

A secure, offline-capable authentication system for distributed executables.

## Architecture

1. **Server**: FastAPI backend that issues OTPs and signs JWTs (RS256).
2. **Client**: Python application (convertible to EXE) that authenticates once and works offline.
3. **Security**:
   - **Transport**: HTTPS (TLS) for all communications.
   - **Token**: RS256 Signed JWT containing User ID, Device ID, and Expiry.
   - **Storage**: Token is encrypted locally using AES (Fernet) with a key derived from the machine's unique Hardware ID.
   - **Offline**: Client verifies signature and expiry locally using embedded Public Key.

## Project Structure

- `server/`: Backend code (FastAPI).
- `client/`: Client code (Python).
- `generate_keys.py`: Utility to generate RSA keys.

## Setup & Installation

1. **Generate Keys**:
   ```bash
   python generate_keys.py
   ```
   This creates `private_key.pem` (keep secure!) and `public_key.pem`.

2. **Server Setup**:
   ```bash
   cd server
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Client Setup**:
   ```bash
   cd client
   pip install -r requirements.txt
   python main.py
   ```

## Deployment

### Server (Railway/Render/DigitalOcean)
1. **Environment**: Python 3.10+.
2. **Files**: Upload `server/` directory and `requirements.txt`.
3. **Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
4. **HTTPS**: Most platforms (Railway, Render) handle SSL automatically.

### Client Distribution
Follow instructions in `client/build_instructions.txt` to package as an EXE.

## Security Features

- **Device Binding**: Tokens are bound to the specific machine hardware. Copying `token.enc` to another machine will fail decryption/validation.
- **Offline Expiry**: Tokens have a hard 24-hour limit checked against the local clock.
- **No Secrets in Client**: Only the Public Key is distributed. The Private Key never leaves the server.

## Testing

### 1. Offline Mode
- Authenticate successfully.
- Disconnect internet.
- Restart app.
- It should still work until expiry.

### 2. Device Mismatch
- Authenticate on Machine A.
- Copy `token.enc` to Machine B.
- Run app on Machine B.
- It should fail (decryption error or device ID mismatch).

### 3. Expiry
- Authenticate.
- Manually change system time to +25 hours.
- Restart app.
- It should deny access.

## Limitations
- **Clock Tampering**: Offline verification relies on client time.
- **Binary Patching**: A skilled attacker with physical access can eventually patch the EXE to bypass checks. Obfuscation (PyArmor) is recommended for production.
