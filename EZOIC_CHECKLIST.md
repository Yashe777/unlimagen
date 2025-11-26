# ✅ Ezoic Integration Checklist for Unlimagen

## 🎯 Quick Setup Checklist

### Pre-Integration (Already Done ✅)
- [x] Added Ezoic meta tag placeholder in HTML
- [x] Added Ezoic script placeholder in HTML  
- [x] Created `/ads.txt` Flask route
- [x] Added 5 strategic ad placeholders on main page
- [x] Added SEO meta tags for better ad performance
- [x] Styled ad placeholders with CSS

### Your Action Items (Do This Now 👇)

#### 1️⃣ Get Info from Ezoic Dashboard
Login to Ezoic and find:
- [ ] Your site verification code
- [ ] Your ads.txt publisher line (e.g., `ezoic.com, pub-123456, DIRECT`)
- [ ] Confirm integration method (Cloudflare or Direct)

#### 2️⃣ Update app.py
Open `app.py` and find line ~424:
```python
@app.route('/ads.txt')
def ads_txt():
    """Serve ads.txt file for Ezoic"""
    from flask import Response
    ads_content = """# Ezoic Ads.txt
# Add your Ezoic publisher line here from Step 2 in Ezoic dashboard
# Example: ezoic.com, pub-XXXXXXXXXXXXX, DIRECT
"""
    return Response(ads_content, mimetype='text/plain')
```

**Replace with your actual line:**
```python
ads_content = """# Ezoic Ads.txt
ezoic.com, pub-YOUR-PUBLISHER-ID, DIRECT
"""
```

#### 3️⃣ Update index_modern.html  
Open `templates/index_modern.html`:

**Line 8 - Add verification code:**
```html
<!-- Change this: -->
<!-- <meta name="ezoic-site-verification" content="YOUR_VERIFICATION_CODE" /> -->

<!-- To this (uncomment and add your code): -->
<meta name="ezoic-site-verification" content="your-actual-code-here" />
```

**Line 20 - Enable Ezoic script:**
```html
<!-- Change this: -->
<!-- <script async src="//www.ezojs.com/ezoic/sa.min.js"></script> -->

<!-- To this (just uncomment): -->
<script async src="//www.ezojs.com/ezoic/sa.min.js"></script>
```

#### 4️⃣ Deploy to Production
```bash
git add .
git commit -m "Add Ezoic integration with publisher ID"
git push origin main
```

#### 5️⃣ Verify Everything Works
- [ ] Visit `https://www.unlimagen.com/ads.txt` - Should show your Ezoic line
- [ ] View page source - Should see Ezoic verification meta tag
- [ ] Check Ezoic dashboard - Should show "Site Verified" (may take 24 hours)

#### 6️⃣ Configure Ad Placements in Ezoic
In Ezoic Dashboard → Placeholders:
- [ ] Enable placeholder 101 (Top Banner) - Suggest: 728x90, 970x90
- [ ] Enable placeholder 102 (Above Content) - Suggest: 300x250
- [ ] Enable placeholder 103 (Right Sidebar) - Suggest: 300x600, 160x600
- [ ] Enable placeholder 104 (Right Sidebar Bottom) - Suggest: 300x250
- [ ] Enable placeholder 105 (Bottom Banner) - Suggest: 728x90

## 🚀 Integration Methods

### Method A: Cloudflare (Easiest - Recommended)
- [ ] Add domain to Cloudflare
- [ ] Point nameservers to Ezoic's Cloudflare nameservers
- [ ] Wait 24-48 hours
- [ ] No additional code changes needed!

### Method B: Direct Integration
- [ ] Add verification meta tag (see step 3 above)
- [ ] Add Ezoic script (see step 3 above)
- [ ] Update ads.txt (see step 2 above)
- [ ] Deploy and verify

## 📊 What to Expect

| Timeline | What Happens |
|----------|--------------|
| Day 0 | Complete integration steps |
| Day 1 | Ezoic verifies site and starts learning |
| Day 2-7 | AI testing different ad placements |
| Day 7+ | Optimized ad performance |
| Day 30+ | Full optimization complete |

## 💰 Revenue Optimization Tips

1. **Drive Traffic**: More visitors = more ad revenue
2. **Quality Content**: Keep your site useful and engaging  
3. **Mobile-Friendly**: Ensure great mobile experience
4. **Page Speed**: Fast sites = better user experience = more revenue
5. **Let Ezoic Optimize**: Don't manually adjust too much at first

## 🆘 Common Issues

### "Site Not Verified"
- Double-check verification code is correct
- Ensure it's in the `<head>` section
- Clear cache and redeploy
- Wait 24 hours

### "Ads.txt Issues"
- Visit `https://www.unlimagen.com/ads.txt`
- Should return plain text (not HTML)
- Should match Ezoic's provided line exactly

### "Ads Not Showing"
- Wait 24-48 hours after verification
- Check browser console for JavaScript errors
- Use Ezoic Chrome extension for debugging
- Verify placeholders are enabled in dashboard

## 📝 Current Ad Placements

Your site now has these ad zones:

1. **Top Banner** (`#ezoic-pub-ad-placeholder-101`)
   - Location: Below navigation, above content
   - Best for: 728x90, 970x90 leaderboard ads
   
2. **Above Content** (`#ezoic-pub-ad-placeholder-102`)
   - Location: In main area, above input form
   - Best for: 300x250 medium rectangle
   
3. **Right Sidebar Top** (`#ezoic-pub-ad-placeholder-103`)
   - Location: Right column, sticky position
   - Best for: 160x600, 300x600 skyscraper
   
4. **Right Sidebar Bottom** (`#ezoic-pub-ad-placeholder-104`)
   - Location: Right column, below top ad
   - Best for: 300x250 medium rectangle
   
5. **Bottom Banner** (`#ezoic-pub-ad-placeholder-105`)
   - Location: Below main content, above footer
   - Best for: 728x90, 970x90 leaderboard ads

## ✨ You're Almost Done!

Just share your Ezoic details and I'll help you update the final configuration! 🎉

**What I Need:**
1. Your Ezoic verification code
2. Your ads.txt line (with publisher ID)
3. Integration method chosen

Then we'll update the files and deploy! 🚀
