# Deploying to DigitalOcean App Platform

## Prerequisites
- A DigitalOcean account.
- A GitHub or GitLab account.
- Git installed locally.

## Steps

### 1. Prepare the Repository
1. Initialize a git repository in the `otpvalidation` folder:
   ```bash
   git init
   ```
2. Create a `.gitignore` file to exclude local secrets and environments:
   ```text
   __pycache__/
   *.pyc
   *.enc
   otp_auth.db
   server/private_key.pem
   server/public_key.pem
   client/public_key.pem
   venv/
   .env
   ```
   > **IMPORTANT**: Never commit `private_key.pem` to a public repository! For production, you should inject this as an Environment Variable.

3. Commit your code:
   ```bash
   git add .
   git commit -m "Initial commit"
   ```

### 2. Configure for DigitalOcean
Create a file named `app.yaml` in the root (optional, or configure via UI):
```yaml
name: otp-auth-server
services:
- name: api
  context_path: server
  run_command: uvicorn main:app --host 0.0.0.0 --port 8080
  envs:
  - key: PRIVATE_KEY
    scope: RUN_TIME
    value: ${PRIVATE_KEY} 
  http_port: 8080
  instance_count: 1
  instance_size_slug: basic-xxs
```
*Note: You'll need to modify `server/auth.py` to read the private key from an env var if it's not a file.*

### 3. Push to GitHub
1. Create a new repository on GitHub.
2. Push your local repo:
   ```bash
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

### 4. Deploy on DigitalOcean
1. Go to [DigitalOcean Apps](https://cloud.digitalocean.com/apps).
2. Click **Create App**.
3. Select **GitHub** as the source and choose your repository.
4. Select the `server` directory as the **Source Directory** (if asked) or root if using `app.yaml`.
5. **Environment Variables**:
   - Add `PRIVATE_KEY` and paste the content of `server/private_key.pem`.
6. **Build Command**: `pip install -r requirements.txt`
7. **Run Command**: `uvicorn main:app --host 0.0.0.0 --port 8080`
8. Click **Next** and **Create Resources**.

Your server will be live at `https://otp-auth-server-xxxx.ondigitalocean.app`.

## Updating the Client
Once deployed, update `SERVER_URL` in `client/main.py` to point to your new HTTPS URL.
