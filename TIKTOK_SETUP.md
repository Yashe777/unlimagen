# TikTok Auto-Poster Setup Guide

## 📋 Requirements

1. **Python 3.8+** installed
2. **TikTok Developer Account**
3. **ffmpeg** installed (for video conversion)
4. **Your Unlimagen website** deployed

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install requests
```

### Step 2: Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Linux:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from: https://ffmpeg.org/download.html

---

## 🎯 TikTok API Setup

### 1. Create TikTok Developer Account

1. Go to: https://developers.tiktok.com/
2. Click "Register" → "Login to Developer Portal"
3. Complete registration

### 2. Create an App

1. In Developer Portal → "Manage Apps" → "Connect an app"
2. Fill in app details:
   - **App name:** Unlimagen Auto Poster
   - **Description:** AI image generator auto poster
3. Submit for review (takes 1-3 days)

### 3. Get Access Token

**After app approval:**

1. Go to your app dashboard
2. Click "Content Posting API"
3. Get your **Client Key** and **Client Secret**
4. Generate **Access Token**:

```python
# Run this once to get your access token
import requests

CLIENT_KEY = "your_client_key"
CLIENT_SECRET = "your_client_secret"

# OAuth flow - follow TikTok documentation
# https://developers.tiktok.com/doc/content-posting-api-get-started
```

5. Copy your **Access Token**
6. Paste it in `tiktok_auto_poster.py`:

```python
TIKTOK_ACCESS_TOKEN = "paste_your_token_here"
```

---

## ⚙️ Configure the Script

Edit `tiktok_auto_poster.py`:

```python
# Your website URL
UNLIMAGEN_URL = "https://unlimagen.com"  # Change if different

# Your TikTok access token
TIKTOK_ACCESS_TOKEN = "YOUR_TOKEN_HERE"
```

---

## 🎨 Add API Endpoint to Your Website

The script needs an API endpoint on your Unlimagen site.

Add this to `app.py`:

```python
@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint for generating images"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        image_type = data.get('image_type', 'Digital Art')
        model = data.get('model', 'miragic')
        
        # Map model names
        model_map = {
            'miragic': 'image',
            'turbo': 'turbo',
            'creative': 'image3'
        }
        
        model_name = model_map.get(model, 'image')
        
        # Generate image URL
        image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?model={model_name}&width=1024&height=1024&seed={random.randint(1, 1000000)}"
        
        return jsonify({
            'success': True,
            'image_url': image_url,
            'prompt': prompt
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

---

## ▶️ Run the Script

### Local Testing:

```bash
python3 tiktok_auto_poster.py
```

### Run in Background:

**Linux/Mac:**
```bash
nohup python3 tiktok_auto_poster.py &
```

**Keep running forever:**
```bash
screen -S tiktok-poster
python3 tiktok_auto_poster.py
# Press Ctrl+A then D to detach
```

---

## ☁️ Deploy to Cloud (24/7 Running)

### Option 1: Render.com (Free)

1. Create `requirements.txt`:
```
requests==2.31.0
```

2. Create `Procfile`:
```
worker: python tiktok_auto_poster.py
```

3. Deploy as "Background Worker"

### Option 2: PythonAnywhere

1. Upload script
2. Run in console
3. Keep alive with scheduled task

---

## 📊 Monitoring

The script prints status messages:

- 🎨 Generating image
- ✅ Image generated
- 📥 Image downloaded
- 🎬 Video created
- 📤 Posting to TikTok
- ✅ Posted successfully

---

## ⚠️ Important Notes

1. **TikTok Rate Limits:**
   - Max 5 posts per day per account
   - Adjust timing if needed

2. **TikTok Requires Video:**
   - Script converts images to 5-second videos
   - Needs ffmpeg installed

3. **Content Policy:**
   - Follow TikTok community guidelines
   - Don't post spam or low-quality content

4. **API Costs:**
   - TikTok API is FREE
   - Your Unlimagen site is FREE
   - Only cost: server/hosting (if any)

---

## 🔧 Troubleshooting

**Error: "TikTok access token not configured"**
- Add your access token to the script

**Error: "ffmpeg not found"**
- Install ffmpeg (see Step 2)

**Error: "Connection refused"**
- Check your UNLIMAGEN_URL is correct
- Make sure website is deployed and accessible

**Error: "TikTok API error 401"**
- Access token expired, regenerate it
- Check token permissions

---

## 📞 Need Help?

If you have issues:
1. Check TikTok API documentation
2. Verify all requirements installed
3. Test Unlimagen API endpoint manually
4. Check script logs for errors

---

## 🎉 Done!

Your TikTok auto-poster is ready! It will:
- Generate AI images every 10 minutes
- Convert to video format
- Post to TikTok automatically
- Run 24/7 in background

Enjoy automated content creation! 🚀
