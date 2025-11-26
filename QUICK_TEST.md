# Quick Test Guide

## 🚀 To Test Payments Right Now:

### Step 1: Get Stripe Test Keys (2 minutes)
1. Go to: https://dashboard.stripe.com/register
2. Sign up (free, no credit card needed)
3. Go to: https://dashboard.stripe.com/test/apikeys
4. Copy your keys

### Step 2: Set Test Environment
Create `ai-image-generator-deploy/.env`:
```
STRIPE_PUBLIC_KEY=pk_test_51...
STRIPE_SECRET_KEY=sk_test_51...
STRIPE_PRICE_BASIC=price_1...
STRIPE_PRICE_PRO=price_1...
```

### Step 3: Create Test Products
1. Go to: https://dashboard.stripe.com/test/products
2. Create "Numidia Basic" - $5/month - copy Price ID
3. Create "Numidia Pro" - $9.99/month - copy Price ID
4. Add Price IDs to .env

### Step 4: Test!
1. Restart server
2. Go to: http://localhost:5002/pricing
3. Click "Get Pro"
4. Use test card: **4242 4242 4242 4242**
5. Any expiry, CVC, ZIP

## 💳 Test Cards:
- **Success:** 4242 4242 4242 4242
- **Decline:** 4000 0000 0000 0002
- **3D Secure:** 4000 0025 0000 3155

Done!
