# Stripe Payment Setup Guide

## Step 1: Create Stripe Account
1. Go to https://stripe.com
2. Click "Start now" to create account
3. Complete verification

## Step 2: Get API Keys
1. Go to https://dashboard.stripe.com/test/apikeys
2. Copy your **Publishable key** (starts with `pk_test_`)
3. Copy your **Secret key** (starts with `sk_test_`)
4. Save these in `.env` file

## Step 3: Create Products & Prices
1. Go to https://dashboard.stripe.com/test/products
2. Click "Add product"

### Basic Plan ($5/month):
- Name: Numidia AI Basic
- Description: 50 images per day
- Price: $5.00 USD
- Billing period: Monthly
- Copy the **Price ID** (starts with `price_`)

### Pro Plan ($9.99/month):
- Name: Numidia AI Pro
- Description: Unlimited images
- Price: $9.99 USD
- Billing period: Monthly
- Copy the **Price ID** (starts with `price_`)

## Step 4: Configure Environment
Create `.env` file:
```
STRIPE_PUBLIC_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PRICE_BASIC=price_basic_id_here
STRIPE_PRICE_PRO=price_pro_id_here
```

## Step 5: Test Payment
1. Use test card: 4242 4242 4242 4242
2. Any future expiry date
3. Any 3-digit CVC
4. Any ZIP code

## Step 6: Go Live
1. Get verified by Stripe
2. Switch to live keys (pk_live_ and sk_live_)
3. Create live products
4. Update .env with live keys
