# TikTok Auto-Poster - Quick Start Guide

## 🎯 What You Need

Based on TikTok's official documentation, here's what you need:

### 1. TikTok Developer Account ✅
- Go to: https://developers.tiktok.com/
- Register and verify your account

### 2. Create Your App ✅
- Click "Manage apps" → "Connect an app"
- Add **Content Posting API** product
- Get approval (1-3 days)

### 3. Get Authorization ✅
You need:
- **Access Token** - Your app's token
- **video.upload scope** - Must be approved
- User must authorize your app

### 4. Verify Your Domain ⚠️
**IMPORTANT:** TikTok requires verified domain for photo posts!

To post photos using `PULL_FROM_URL`, you must:
1. Verify your domain at: https://developers.tiktok.com/
2. Add verification meta tag to your website
3. Or upload verification file

**Without verified domain:**
- Photos won't work with `PULL_FROM_URL`
- Must use video upload with `FILE_UPLOAD` method

---

## 🚀 Two Methods to Post

### Method 1: Photo Posts (Recommended)
✅ **Easier** - No video conversion needed
✅ **Faster** - Direct upload
❌ **Requires** - Verified domain

**How it works:**
1. Generate image on Unlimagen
2. Image URL must be from verified domain
3. Post directly to TikTok as photo carousel
4. Goes live immediately (or to draft)

### Method 2: Video Posts (Fallback)
✅ **Works without domain verification**
✅ **More compatible**
❌ **Slower** - Needs video conversion (ffmpeg)
❌ **Goes to inbox** - User must approve in TikTok app

**How it works:**
1. Generate image on Unlimagen
2. Convert image to 5-second video (ffmpeg)
3. Upload video file to TikTok
4. User sees notification in TikTok inbox
5. User reviews and posts manually

---

## ⚙️ Setup Steps

### Step 1: Domain Verification (For Photo Posts)

**Option A: Meta Tag Method**
1. Go to TikTok Developer Portal
2. Enter: `unlimagen.com`
3. Copy verification meta tag
4. Add to your website `<head>`:
```html
<meta name="tiktok-for-developers" content="YOUR_VERIFICATION_CODE" />
```
5. Click "Verify"

**Option B: File Upload Method**
1. Download verification file
2. Upload to: `https://unlimagen.com/tiktok-verify.txt`
3. Click "Verify"

### Step 2: Get Access Token

**OAuth Flow (Recommended):**
```python
# User authorizes your app
# You get access token
# Token expires after 24 hours (refresh needed)
```

**For Testing:**
- Use Developer Token from app dashboard
- Valid for 1-3 months
- Manual refresh needed

### Step 3: Configure Script

Edit `tiktok_auto_poster.py`:

```python
UNLIMAGEN_URL = "https://unlimagen.com"
TIKTOK_ACCESS_TOKEN = "act.your_actual_token_here"
VERIFIED_DOMAIN = "https://unlimagen.com"  # Must be verified!
```

### Step 4: Install Requirements

```bash
# Python packages
pip install requests

# For video conversion (Method 2 only)
# Mac:
brew install ffmpeg

# Ubuntu:
sudo apt-get install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
```

### Step 5: Run!

```bash
python3 tiktok_auto_poster.py
```

---

## 📊 What Happens

**Every 10 minutes:**
1. 🎨 Generate random AI image
2. 📤 Try to post as photo (Method 1)
3. 🔄 If fails, convert to video (Method 2)
4. ✅ Post to TikTok
5. ⏳ Wait 10 minutes
6. 🔁 Repeat

**You'll see:**
```
🚀 TikTok Auto-Poster Started!
⏰ Posting every 10 minutes
--------------------------------------------------

📍 Post #1 - 2024-01-15 10:30:00
🎨 Generating image: A futuristic city at sunset (Digital Art)
✅ Image generated: https://image.pollinations.ai/...
📥 Image downloaded: ai_image_1234567890.png
📤 Posting photo to TikTok...
✅ Photo posted to TikTok! Publish ID: p_pub_url~v2.123456789

⏳ Waiting 10 minutes until next post...
```

---

## ⚠️ Important Notes

### Rate Limits
- **TikTok limits:** ~5 posts per day per account
- **Recommended:** Post every 2-4 hours (not 10 minutes!)
- Adjust in script: `time.sleep(7200)  # 2 hours`

### Post Modes
- **DIRECT_POST** - Goes live immediately
- **MEDIA_UPLOAD** - Goes to draft/inbox for review

### Content Guidelines
- Follow TikTok community guidelines
- No spam or repetitive content
- Quality over quantity

### Token Expiration
- Access tokens expire (24 hours - 3 months)
- Need to refresh periodically
- Implement OAuth refresh flow for production

---

## 🔧 Troubleshooting

**Error: "Domain not verified"**
- Complete domain verification first
- Use video method as fallback

**Error: "Invalid access token"**
- Token expired, get new one
- Check token has `video.upload` scope

**Error: "Rate limit exceeded"**
- TikTok daily limit reached
- Wait 24 hours or reduce frequency

**Error: "ffmpeg not found"**
- Install ffmpeg for video conversion
- Or use photo method only

**Photos not posting:**
- Check domain is verified
- Image URL must be from verified domain
- Use video method as alternative

---

## 🎯 Next Steps

1. **Get TikTok API access** (apply now!)
2. **Verify your domain** (for photo posts)
3. **Get access token** (from app dashboard)
4. **Add token to script**
5. **Run and test!**

---

## 💡 Pro Tips

- Start with video method (easier setup)
- Add domain verification later for photo posts
- Monitor TikTok inbox for video uploads
- Adjust posting frequency based on engagement
- Use diverse prompts for variety
- A/B test different captions

---

## 📞 Need Help?

Check:
1. TikTok API docs: https://developers.tiktok.com/doc/content-posting-api-get-started
2. Script logs for error messages
3. TikTok Developer Portal for app status

Good luck! 🚀
