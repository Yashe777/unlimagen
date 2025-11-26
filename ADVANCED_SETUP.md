# 🎥 Advanced TikTok Video Automation Setup

## What This Does

Creates **30-second motivational TikTok videos** automatically:

✅ **Detects trending topics** (AI, productivity, motivation, etc.)
✅ **Generates video scripts** (hooks, points, call-to-action)
✅ **Creates multiple AI images** (3-5 images per video)
✅ **Adds AI voiceover** (natural human-like voice)
✅ **Combines into 30s video** (vertical format 1080x1920)
✅ **Auto-posts to TikTok** (every 4 hours)

---

## 📋 Requirements

### 1. Python & FFmpeg
```bash
# Install Python packages
pip install requests

# Install FFmpeg (video editing)
# Mac:
brew install ffmpeg

# Ubuntu:
sudo apt-get install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
```

### 2. API Keys (3 services)

#### A. TikTok API ✅ (Required)
- **Purpose:** Post videos to TikTok
- **Cost:** FREE
- **Setup:** See TIKTOK_QUICK_START.md
- Get from: https://developers.tiktok.com/

#### B. ElevenLabs API 🎙️ (For Voice)
- **Purpose:** Generate AI voiceover
- **Cost:** Free tier: 10,000 characters/month
- **Setup:**
  1. Go to: https://elevenlabs.io
  2. Sign up (free)
  3. Go to Profile → API Keys
  4. Copy your API key
  
**Alternative (Free):**
- Skip voiceover (videos work without it)
- Use text overlays instead

#### C. OpenAI API 🤖 (For Smart Scripts)
- **Purpose:** Generate trending scripts with AI
- **Cost:** ~$0.002 per script (very cheap)
- **Setup:**
  1. Go to: https://platform.openai.com/
  2. Create account
  3. Add payment method ($5 minimum)
  4. Go to API Keys → Create
  5. Copy key

**Alternative (Free):**
- Use built-in templates (works great!)
- Script will still customize topics

---

## ⚙️ Configuration

Edit `tiktok_video_automation.py`:

```python
# Required
TIKTOK_ACCESS_TOKEN = "act.your_token_here"

# Optional (for better quality)
ELEVENLABS_API_KEY = "your_elevenlabs_key"  # For voice
OPENAI_API_KEY = "sk-your_openai_key"  # For smart scripts

# Your website
UNLIMAGEN_URL = "https://unlimagen.com"
```

---

## 🚀 How It Works

### Video Creation Process:

**1. Select Trending Topic** (Random from 15+ categories)
- AI Technology
- Self Improvement
- Productivity Hacks
- Mental Health
- Success Mindset
- etc.

**2. Generate Script** (30 seconds)
```
[0-3s] Hook: "Did you know AI can now do THIS?"
[3-12s] Point 1: "AI can generate images in seconds"
[12-21s] Point 2: "It can write code and create music"
[21-27s] Point 3: "The future is accessible to everyone"
[27-30s] CTA: "Try it free at Unlimagen.com!"
```

**3. Generate Images** (3-5 per video)
- Each segment gets unique AI image
- Generated from Unlimagen
- Related to script content

**4. Create Voiceover** (Optional)
- Natural AI voice
- Reads entire script
- Synced with video

**5. Combine Everything**
- Images transition smoothly
- Audio overlaid
- Vertical format (TikTok standard)
- 30 seconds exactly

**6. Upload to TikTok**
- Auto-posts every 4 hours
- Hashtags added automatically
- User reviews in TikTok inbox

---

## 🎬 Video Output Example

**Video Structure:**
```
[0-6s]   Image 1: Hook visual
[6-12s]  Image 2: Point 1 visual  
[12-18s] Image 3: Point 2 visual
[18-24s] Image 4: Point 3 visual
[24-30s] Image 5: CTA visual

+ AI Voiceover narrating throughout
+ Smooth transitions
+ Vertical 1080x1920 format
```

**Caption:**
```
AI Technology 💡✨ #motivation #ai #inspiration #fyp
```

---

## ▶️ Running the Automation

### Test Run (Create 1 Video):
```bash
python3 tiktok_video_automation.py
```

Watch the output:
```
🚀 Starting video creation - 10:30:00
==================================================
📊 Topic: AI Technology
📝 Generating script...
✅ Script created with 5 segments
🎨 Generating image 1/5: Did you know AI can now...
✅ Image 1 generated
🎨 Generating image 2/5: AI can generate images...
✅ Image 2 generated
...
🎙️ Generating voiceover...
✅ Voiceover generated: voiceover_1234.mp3
🎬 Creating video...
✅ Video created: tiktok_video_1234.mp4
📤 Uploading to TikTok...
✅ Video uploaded! Publish ID: v_inbox_file~v2.123
📱 User will see notification in TikTok inbox
✅ Video #1 posted successfully!

⏳ Waiting 4 hours until next video...
```

### Run 24/7 (Background):
```bash
# Linux/Mac
nohup python3 tiktok_video_automation.py &

# Or use screen
screen -S tiktok
python3 tiktok_video_automation.py
# Press Ctrl+A then D to detach
```

---

## 🎨 Customization

### Change Topics
Edit the `categories` list:
```python
categories = [
    "Your Topic 1",
    "Your Topic 2",
    "Your Topic 3"
]
```

### Add Custom Scripts
Edit `templates` dictionary:
```python
templates = {
    "Your Topic": {
        "hook": "Your hook",
        "points": ["Point 1", "Point 2", "Point 3"],
        "cta": "Your call to action"
    }
}
```

### Change Posting Frequency
```python
# Post every 2 hours (6 videos/day)
auto_post_loop(interval_hours=2)

# Post every 6 hours (4 videos/day)
auto_post_loop(interval_hours=6)
```

### Change Video Duration
```python
# 15-second videos
duration_per_image = 15 / len(images)
'-t', '15'

# 60-second videos
duration_per_image = 60 / len(images)
'-t', '60'
```

---

## 💰 Cost Breakdown

**With All Features:**
- TikTok API: **FREE**
- ElevenLabs (voice): **FREE** (10k chars/month)
- OpenAI (scripts): **~$0.50/month** (250 videos)
- Hosting: **FREE** (Render.com)

**Total: ~$0.50/month or FREE**

**Without Optional APIs:**
- TikTok API: **FREE**
- Templates instead of OpenAI: **FREE**
- No voiceover: **FREE**
- Hosting: **FREE**

**Total: $0/month (100% FREE)**

---

## 📊 Expected Results

**With 4 videos/day:**
- **120 videos/month**
- **Consistent content**
- **Trending topics**
- **Professional quality**

**Potential Growth:**
- Start: 0-100 followers
- Month 1: 100-500 followers
- Month 3: 500-2,000 followers
- Month 6: 2,000-10,000 followers

*Results vary based on content quality and engagement*

---

## 🔧 Troubleshooting

**"FFmpeg not found"**
- Install ffmpeg (see Requirements)

**"No images generated"**
- Check Unlimagen URL is correct
- Add API endpoint to app.py (see TIKTOK_SETUP.md)

**"Voiceover failed"**
- Check ElevenLabs API key
- Or disable voiceover (videos work without it)

**"TikTok upload failed"**
- Check access token is valid
- Verify video.upload scope enabled
- Check video file size < 500MB

**"Script generation failed"**
- Check OpenAI API key
- Or system uses templates automatically

---

## 🎯 Pro Tips

1. **Start without voice** - Test with images only first
2. **Use templates** - Free and works great
3. **Post 4-6 times/day** - Optimal for TikTok algorithm
4. **Mix topics** - Variety keeps audience engaged
5. **Monitor engagement** - Adjust based on what works
6. **Add trending sounds** - Manually in TikTok app for better reach

---

## 📱 Workflow Summary

```
Every 4 hours:
1. Pick trending topic
2. Generate script (AI or template)
3. Create 5 AI images
4. Generate voiceover (optional)
5. Combine into 30s video
6. Upload to TikTok
7. User reviews & posts
8. Repeat!
```

---

## 🚀 Deploy to Cloud (24/7)

### Render.com (Free)

1. Create `requirements.txt`:
```
requests==2.31.0
```

2. Create `Procfile`:
```
worker: python tiktok_video_automation.py
```

3. Push to GitHub
4. Connect to Render as "Background Worker"
5. Add environment variables (API keys)

---

## 🎉 You're Ready!

**Next steps:**
1. Get API keys (TikTok required, others optional)
2. Configure the script
3. Test with one video
4. Deploy and automate!

**Questions? Check:**
- TIKTOK_QUICK_START.md
- TIKTOK_SETUP.md
- Script comments

Good luck with your viral content! 🚀📈
