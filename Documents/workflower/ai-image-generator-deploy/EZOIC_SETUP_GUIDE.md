# 🚀 Ezoic Setup Guide for Unlimagen

This guide will help you complete the Ezoic integration step by step.

## ✅ What We've Already Done

1. ✅ Added SEO meta tags for better ad performance
2. ✅ Added Ezoic script placeholders in `<head>` section
3. ✅ Created `/ads.txt` route in Flask app
4. ✅ Added 5 strategic ad placeholders throughout the site:
   - **Placeholder 101**: Top horizontal banner (728x90 or responsive)
   - **Placeholder 102**: Above main content (300x250 square)
   - **Placeholder 103**: Right sidebar top (160x600 or 300x600 skyscraper)
   - **Placeholder 104**: Right sidebar bottom (300x250 square)
   - **Placeholder 105**: Bottom content (728x90 or responsive)

## 📋 Steps to Complete in Ezoic Dashboard

### **Step 1: Site Integration**

Go to your Ezoic dashboard and check which integration method they recommend:

#### Option A: Cloudflare Integration (Recommended - Easiest)
1. Go to Ezoic Dashboard → Integration
2. Select "Cloudflare Integration"
3. Change your domain's nameservers to Ezoic's nameservers
4. Wait 24-48 hours for DNS propagation
5. No code changes needed - Ezoic will inject ads automatically

#### Option B: Direct Integration (Manual)
1. Get your Ezoic Site Verification Code from the dashboard
2. Update `templates/index_modern.html` line 8:
   ```html
   <!-- Replace this line: -->
   <!-- <meta name="ezoic-site-verification" content="YOUR_VERIFICATION_CODE" /> -->
   
   <!-- With your actual code: -->
   <meta name="ezoic-site-verification" content="your-actual-code-here" />
   ```
3. Get your Ezoic JavaScript snippet (usually looks like):
   ```html
   <script async src="//www.ezojs.com/ezoic/sa.min.js"></script>
   ```
4. Uncomment line 20 in `templates/index_modern.html` and verify it matches your code

### **Step 2: Ads.txt Setup**

1. Go to Ezoic Dashboard → Ads.txt Management
2. Copy the ads.txt line provided by Ezoic (looks like):
   ```
   ezoic.com, pub-1234567890123456, DIRECT
   ```
3. Update `app.py` (around line 424):
   ```python
   ads_content = """# Ezoic Ads.txt
   ezoic.com, pub-YOUR-PUBLISHER-ID, DIRECT
   """
   ```
4. Verify at: `https://www.unlimagen.com/ads.txt`

### **Step 3: Ad Placements**

We've already added 5 ad placeholder divs with IDs:
- `ezoic-pub-ad-placeholder-101` (Top Banner)
- `ezoic-pub-ad-placeholder-102` (Above Content)
- `ezoic-pub-ad-placeholder-103` (Right Sidebar Top)
- `ezoic-pub-ad-placeholder-104` (Right Sidebar Bottom)
- `ezoic-pub-ad-placeholder-105` (Bottom Banner)

In Ezoic Dashboard:
1. Go to **Ad Tester** or **Placeholders**
2. Ezoic should automatically detect these placeholder divs
3. Enable the placeholders you want to use
4. Configure ad sizes for each placeholder:
   - 101, 105: 728x90, 970x90, or responsive
   - 102, 104: 300x250, 336x280
   - 103: 160x600, 300x600, or 300x250

### **Step 4: Dynamic Content Setup**

Your site generates images dynamically. Tell Ezoic:
1. Go to **Settings** → **Advanced Settings**
2. Enable "Dynamic Content" or "AJAX Support"
3. This ensures ads refresh properly when users generate new images

### **Step 5: Testing**

After integration:
1. Clear your browser cache
2. Visit `https://www.unlimagen.com`
3. Check if ads appear (may take 24-48 hours initially)
4. Test ad placeholders show properly
5. Use Ezoic's Chrome extension to see ad diagnostics

## 🔧 Quick Actions Needed

### Action 1: Get Your Ezoic Details
Login to your Ezoic dashboard and copy:
- [ ] Site verification code (if using direct integration)
- [ ] Ads.txt line with your publisher ID
- [ ] Integration method chosen (Cloudflare or Direct)

### Action 2: Update Files
Once you have the details above, update:

**File: `app.py` (line ~424)**
```python
ads_content = """# Ezoic Ads.txt
ezoic.com, pub-YOUR-ACTUAL-PUBLISHER-ID, DIRECT
"""
```

**File: `templates/index_modern.html` (lines 7-8)**
```html
<!-- Uncomment and add your verification code -->
<meta name="ezoic-site-verification" content="your-actual-verification-code" />
```

**File: `templates/index_modern.html` (line 20)**
```html
<!-- Uncomment this line -->
<script async src="//www.ezojs.com/ezoic/sa.min.js"></script>
```

### Action 3: Deploy Changes
After updating the files:
```bash
git add .
git commit -m "Add Ezoic integration"
git push origin main
```

Wait for deployment to complete on Render.

### Action 4: Verify Integration
1. Visit `https://www.unlimagen.com/ads.txt` - should show your Ezoic line
2. View page source - should see Ezoic meta tag and script
3. Check Ezoic dashboard - should show "Site Verified"

## 📊 Expected Timeline

- **Day 0**: Complete integration steps above
- **Day 1-2**: Ezoic verifies your site and starts testing
- **Day 3-7**: Ad optimization period (Ezoic tests different placements)
- **Day 7+**: Stable ad performance and revenue

## 💡 Tips for Better Earnings

1. **Content Quality**: Your site is great - keep it user-friendly
2. **Traffic**: More visitors = more revenue (promote your site!)
3. **Ad Balance**: Ezoic will optimize ad density automatically
4. **User Experience**: Don't add too many manual ads
5. **Mobile**: Ensure site works great on mobile (Ezoic handles responsive ads)

## 🆘 Troubleshooting

### Ads Not Showing?
- Wait 24-48 hours after integration
- Check browser console for errors
- Verify ads.txt is accessible
- Check Ezoic dashboard for status

### Verification Failed?
- Ensure meta tag is in `<head>` section
- Clear cache and redeploy
- Check for typos in verification code

### Low Revenue?
- Give it 7-14 days for optimization
- Increase traffic to your site
- Ensure content is advertiser-friendly
- Check Ezoic's optimization suggestions

## 📞 Need Help?

If you need assistance:
1. Share your Ezoic verification code
2. Share your ads.txt line
3. Let me know which integration method you chose
4. I'll help you update the files correctly!

## 🎉 Next Steps

Once Ezoic is fully integrated:
- [ ] Monitor earnings in Ezoic dashboard
- [ ] Use Ezoic's AI to optimize ad placements
- [ ] Test different ad configurations
- [ ] Focus on driving traffic to your site
- [ ] Consider Ezoic's premium features (Level Up)

---

**Current Status**: Ready for you to add Ezoic credentials and deploy! 🚀
