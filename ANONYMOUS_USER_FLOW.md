# Anonymous User Flow - 10 Free Daily Images

## 🎉 Feature Overview

Your website now allows **anonymous users** (visitors who haven't signed up) to generate **10 FREE images per day** without creating an account!

## 📊 How It Works

### 1. **First Visit (No Signup Required)**
- User opens your website
- User enters a prompt and clicks "Generate"
- Images are generated immediately
- No login/signup required!

### 2. **Usage Tracking**
- Anonymous users are tracked by **IP address**
- Each IP gets **10 free images per day**
- Counter resets at midnight (daily)
- Usage data stored in `usage_data.json`

### 3. **When Limit is Reached**
After generating 10 images, when the user tries to generate #11:

**A beautiful modal appears showing:**

```
🎨 You've Used Your 10 Free Images!

Create a free account to track your usage and get 10 more images tomorrow!
Upgrade to Basic (50/day) or Pro (unlimited) plans.

┌─────────────────────────────────────┐
│ You just used:                      │
│ 10 FREE images (IP-based)           │
└─────────────────────────────────────┘

[Sign Up Free →]  [View Pricing Plans]

Close
```

## 🔧 Technical Implementation

### Backend (app.py)
```python
# Lines 420-459 in app.py
if user_email:
    # Logged in user
    user = db.get_user(user_email)
    tier = user['plan']
    daily_limit = user['daily_limit']
else:
    # Anonymous user - IP-based tracking
    tier = 'free'
    daily_limit = 10

# Check rate limit
can_generate, remaining = rate_limiter.check_limit(
    ip_address, 
    user_id=user_email, 
    tier=tier
)

if not can_generate:
    if not user_email:
        # Show signup modal for anonymous users
        return jsonify({
            'success': False,
            'limit_reached': True,
            'need_signup': True,
            'message': 'You have reached your daily limit of 10 free images. Sign up to track your usage and upgrade for more!'
        }), 429
```

### Frontend (index_modern.html)
```javascript
// Lines 1402-1408
if (response.status === 429 || data.limit_reached) {
    if (data.need_signup) {
        showSignupModal();  // For anonymous users
    } else {
        showLimitModal();   // For logged-in free users
    }
    return;
}
```

### Modal Display (index_modern.html)
```javascript
// Lines 1234-1263
function showSignupModal() {
    // Creates a beautiful modal with:
    // - 🎨 Emoji icon
    // - Usage counter (10 FREE images)
    // - "Sign Up Free" button
    // - "View Pricing Plans" link
    // - Close button
}
```

## 📋 User Journey

### Anonymous User Journey:
```
1. Visit website
   ↓
2. Enter prompt → Generate images (1/10)
   ↓
3. Generate more images... (2/10, 3/10... 9/10)
   ↓
4. Try to generate 11th image
   ↓
5. 🎨 Modal appears: "You've Used Your 10 Free Images!"
   ↓
6. Two options:
   A) Sign Up Free → Get account + 10 more tomorrow
   B) View Pricing → Upgrade to 50/day or unlimited
```

### Logged-in Free User Journey:
```
1. Login to account
   ↓
2. Generate images (tracked by user account)
   ↓
3. Use all 10 daily images
   ↓
4. ⚠️ Modal appears: "Daily Limit Reached!"
   ↓
5. Option: View Pricing Plans → Upgrade
```

## 🎯 Benefits

### For Users:
✅ **No signup barrier** - Start creating immediately  
✅ **10 free images daily** - Try before committing  
✅ **Clear upgrade path** - See pricing when interested  
✅ **Account benefits** - Persistent tracking after signup  

### For You (Business):
✅ **Lower friction** - Users can try instantly  
✅ **Natural conversion** - Modal appears at right moment  
✅ **Abuse prevention** - IP-based rate limiting  
✅ **Upsell opportunity** - Show pricing at limit  

## 🔐 Rate Limits

| User Type | Daily Limit | Tracking Method |
|-----------|-------------|-----------------|
| Anonymous | 10 images   | IP Address      |
| Free Account | 10 images | User Email   |
| Basic Plan | 50 images  | User Email      |
| Pro Plan | Unlimited   | User Email      |

## 📱 Mobile Responsive

The signup modal is **fully responsive** and looks great on:
- Desktop computers
- Tablets
- Mobile phones

## 🔄 Daily Reset

Limits reset automatically at **midnight** (server time) every day:
- Anonymous users get 10 new images
- Free accounts get 10 new images
- Basic accounts get 50 new images
- Pro accounts remain unlimited

## 🚀 Already Implemented!

**Good news!** This feature is **already fully working** in your codebase:

✅ Backend rate limiting (`rate_limiter.py`)  
✅ IP-based tracking for anonymous users  
✅ API endpoint logic (`app.py`)  
✅ Frontend modal display (`index_modern.html`)  
✅ Beautiful UI/UX with signup encouragement  
✅ Mobile responsive design  

## 🧪 Testing

Run the test script to verify:
```bash
python3 tmp_rovodev_test_flow.py
```

This will simulate:
1. 10 successful anonymous generations
2. 11th attempt triggering the signup modal
3. Verification of rate limit logic

## 📝 Summary

Your website now has a **perfect freemium model**:
1. **Try for free** (10 images, no signup)
2. **Sign up** (track usage, get 10 daily)
3. **Upgrade** (50/day or unlimited)

This maximizes user acquisition while still encouraging signups and upgrades! 🎉
