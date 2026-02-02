# 🚀 Deploy to Render.com (Free)

## Step 1: Push to GitHub
✅ Already done! Code is at: https://github.com/manish62072/rock-paper-scissors-game

## Step 2: Create Render Account
1. Go to https://render.com
2. Click "Sign Up"
3. Sign up with GitHub (quickest)
4. Authorize Render to access your GitHub

## Step 3: Deploy the App
1. Visit: https://dashboard.render.com/new/web-service
2. Configure:
   - **Owner**: Your GitHub account
   - **Repository**: `manish62072/rock-paper-scissors-game`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (select "Free" at the bottom)

3. Click "Create Web Service"

## Step 4: Add Environment Variables
After the service is created:
1. Click "Environment" tab on the left
2. Add a new secret:
   - Key: `SECRET_KEY`
   - Value: `any-random-string-like-this-12345`
3. Click "Save Changes"

## Step 5: Access Your App!
Your app will be live at: `https://rock-paper-scissors-game-xxxx.onrender.com`

The URL will be shown in your Render dashboard.

---

## Alternative: Deploy to Railway.app
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `manish62072/rock-paper-scissors-game`
5. Railway auto-detects Flask
6. Add `SECRET_KEY` environment variable
7. Click Deploy!

Your URL will be like: `https://rock-paper-scissors-game.up.railway.app`

