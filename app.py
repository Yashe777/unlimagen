"""
Free AI Logo Generator - FIXED VERSION
Uses Pollinations.AI - completely free, no API key needed!
"""

from flask import Flask, render_template, request, jsonify, redirect, session, url_for
import random
import colorsys
import requests
import base64
from datetime import datetime
from urllib.parse import quote
from rate_limiter import rate_limiter
from database import db
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Disable template caching for production updates
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# PayPal Configuration
PAYPAL_BUSINESS_EMAIL = "mr.oudesign@gmail.com"

# Plan Prices
PLANS = {
    'basic': {'name': 'Numidia AI Basic', 'price': '5.00', 'limit': 50},
    'pro': {'name': 'Numidia AI Pro', 'price': '9.99', 'limit': -1}
}

# Logo styles and color schemes
LOGO_STYLES = [
    'minimal', 'geometric', 'circular', 'badge', 'wordmark', 
    'lettermark', 'abstract', 'mascot', 'emblem', 'combination'
]

COLOR_SCHEMES = {
    'professional': ['#2C3E50', '#3498DB', '#ECF0F1'],
    'vibrant': ['#E74C3C', '#F39C12', '#9B59B6'],
    'nature': ['#27AE60', '#16A085', '#F39C12'],
    'elegant': ['#34495E', '#95A5A6', '#BDC3C7'],
    'modern': ['#1ABC9C', '#3498DB', '#9B59B6'],
    'warm': ['#E74C3C', '#E67E22', '#F39C12'],
    'cool': ['#3498DB', '#9B59B6', '#1ABC9C'],
    'monochrome': ['#2C3E50', '#7F8C8D', '#ECF0F1']
}

# FREE AI Services (no API key needed!)
FREE_AI_SERVICES = {
    'stable-horde': {
        'name': 'Stable Horde ⭐ (FREE)',
        'description': 'BEST for complex prompts! Handles all elements, premium quality',
        'speed': 'Medium (30-60s)',
        'quality': '⭐⭐⭐⭐⭐⭐',
        'endpoint': 'https://stablehorde.net/api/v2',
        'model_id': 'Deliberate/Realistic Vision/DreamShaper',
        'recommended': True
    },
    'miragic': {
        'name': 'Miragic AI (FREE)',
        'description': 'Advanced image generation from Hugging Face',
        'speed': 'Fast (5-10s)',
        'quality': '⭐⭐⭐⭐⭐',
        'endpoint': 'https://api-inference.huggingface.co/models/mukaist/Miragic-AI',
        'model_id': 'mukaist/Miragic-AI'
    },
    'pollinations': {
        'name': 'Pollinations.AI (FREE)',
        'description': 'Fast, reliable, no limits',
        'speed': 'Fast (3-5s)',
        'quality': '⭐⭐⭐⭐⭐',
        'endpoint': 'https://image.pollinations.ai/prompt/{prompt}'
    },
    'wan25': {
        'name': 'Turbo AI (FREE)',
        'description': 'Fast, realistic, high quality',
        'speed': 'Fast (3-5s)',
        'quality': '⭐⭐⭐⭐⭐',
        'endpoint': 'turbo'
    }
}

# Style descriptions
STYLE_DESCRIPTIONS = {
    'minimal': 'minimalist, simple, clean lines, modern',
    'geometric': 'geometric shapes, structured, angular',
    'circular': 'circular design, round, balanced',
    'badge': 'badge style, seal, traditional',
    'wordmark': 'typography-focused, elegant',
    'lettermark': 'monogram, initials, sophisticated',
    'abstract': 'abstract, artistic, creative',
    'mascot': 'character design, friendly',
    'emblem': 'shield, crest, formal',
    'combination': 'icon and text, professional'
}

COLOR_DESCRIPTIONS = {
    'professional': 'blue and gray, corporate',
    'vibrant': 'vibrant bold colors, energetic',
    'nature': 'green and earth tones, organic',
    'elegant': 'sophisticated muted colors, luxury',
    'modern': 'teal and purple, contemporary',
    'warm': 'warm colors, friendly',
    'cool': 'cool colors, calm',
    'monochrome': 'black and white, classic'
}

def create_logo_prompt(company_name, style, industry, color_scheme, variation=0, background='natural'):
    """Create optimized prompt for AI logo generation with variations"""
    
    style_desc = STYLE_DESCRIPTIONS.get(style, 'modern, professional')
    color_desc = COLOR_DESCRIPTIONS.get(color_scheme, 'harmonious colors')
    industry_context = f", {industry} industry" if industry else ""
    
    # Add variation keywords to make each logo unique
    variations = [
        "elegant and refined",
        "bold and striking", 
        "creative and artistic",
        "sleek and contemporary",
        "unique and memorable",
        "sophisticated and timeless"
    ]
    
    variation_text = variations[variation % len(variations)]
    
    # Background descriptions based on user choice
    background_styles = {
        'white': 'white background, centered, clean, simple, isolated on white',
        'natural': 'natural background, realistic environment, atmospheric, detailed scene',
        'creative': 'artistic background, creative composition, dynamic, visually striking'
    }
    
    background_desc = background_styles.get(background, background_styles['natural'])
    
    # Add random seed to URL for more variation
    seed = random.randint(1, 999999)
    
    prompt = f"{company_name}{industry_context}, {style_desc}, {color_desc}, {variation_text}, {background_desc}, high quality, detailed, professional, seed {seed}"
    
    return prompt

def generate_with_miragic(prompt, seed=None):
    """Generate using Miragic AI style via Pollinations - Completely FREE! Uses full prompts"""
    try:
        # Use Pollinations with optimized prompt for Miragic-style results
        # USE FULL PROMPT like server.py
        enhanced_prompt = prompt + ", highly detailed, professional, award-winning"
        encoded_prompt = quote(enhanced_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        if seed is None:
            seed = random.randint(1, 999999)
        
        print(f"Generating with Miragic AI style (seed: {seed})...")
        print(f"Full Prompt: {enhanced_prompt[:100]}...")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            image_bytes = response.content
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            print("✅ Success with Miragic AI!")
            return f"data:image/jpeg;base64,{image_base64}"
        else:
            raise Exception(f"HTTP {response.status_code}")
            
    except Exception as e:
        raise Exception(f"Miragic AI error: {str(e)}")

def generate_with_pollinations(prompt, seed=None, model='flux'):
    """Generate using Pollinations.AI - Completely FREE! Multiple endpoints for load balancing"""
    try:
        # Add seed for variation - this ensures different images
        if seed is None:
            seed = random.randint(1, 999999)
        
        # Pollinations.AI - Use the main working endpoint
        encoded_prompt = quote(prompt)
        
        # Use the reliable endpoint (others were causing redirects and failures)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
        
        print(f"Generating with Pollinations.AI (seed: {seed}, endpoint: {url.split('/')[2]})...")
        print(f"Full Prompt: {prompt[:100]}...")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            # Convert to base64
            image_bytes = response.content
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            print("✅ Success with full prompt!")
            return f"data:image/jpeg;base64,{image_base64}"
        elif response.status_code == 429:
            # Rate limit hit
            raise Exception("⏱️ Numidia Creative is currently experiencing high demand. Please try again in a moment, or switch to Numidia Imagine for instant results!")
        elif response.status_code >= 500:
            # Server error
            raise Exception("🔧 Numidia Creative is temporarily unavailable due to high traffic. Please try Numidia Imagine instead!")
        else:
            raise Exception(f"⚠️ Numidia Creative is busy (Error {response.status_code}). Please try Numidia Imagine for better availability!")
            
    except requests.exceptions.Timeout:
        raise Exception("⏱️ Numidia Creative is experiencing high demand and timed out. Please switch to Numidia Imagine for faster generation!")
    except requests.exceptions.RequestException as e:
        raise Exception("🔧 Numidia Creative is currently overloaded. Please try Numidia Imagine instead!")
    except Exception as e:
        if "429" in str(e) or "rate" in str(e).lower():
            raise Exception("⏱️ Numidia Creative is experiencing high demand. Please try Numidia Imagine for instant results!")
        raise Exception(f"⚠️ Numidia Creative is temporarily unavailable. Please try Numidia Imagine instead!")

def generate_with_stable_horde(prompt, seed=None):
    """Generate using Stable Horde - BEST for complex prompts with premium quality!"""
    import time
    import urllib.parse
    
    try:
        # Enhanced prompt with quality keywords
        enhanced_prompt = f"{prompt}, highly detailed, sharp focus, intricate details, masterpiece, best quality, professional, perfect composition, crystal clear, ultra detailed, photorealistic"
        
        negative_prompt = "blurry, blur, low quality, bad quality, distorted, deformed, ugly, watermark, text, error, artifacts"
        
        # Submit generation request
        submit_url = "https://stablehorde.net/api/v2/generate/async"
        headers = {
            "Content-Type": "application/json",
            "apikey": "0000000000"
        }
        
        payload = {
            "prompt": enhanced_prompt,
            "params": {
                "width": 384,
                "height": 384,
                "steps": 35,
                "n": 1,
                "sampler_name": "k_euler",
                "cfg_scale": 8.5,
                "karras": True
            },
            "nsfw": False,
            "trusted_workers": True,
            "slow_workers": True,
            "models": ["Deliberate", "Realistic Vision V5.0", "DreamShaper", "stable_diffusion"]
        }
        
        if negative_prompt:
            payload["params"]["negative_prompt"] = negative_prompt
        
        print(f"🎨 Submitting to Stable Horde (premium quality)...")
        print(f"Prompt: {prompt[:80]}...")
        
        response = requests.post(submit_url, json=payload, headers=headers, timeout=30)
        
        if response.status_code not in [200, 202]:
            raise Exception(f"Submission failed: {response.status_code}")
        
        result = response.json()
        request_id = result.get("id")
        
        if not request_id:
            raise Exception("No request ID received")
        
        print(f"✅ Request ID: {request_id}, waiting for generation...")
        
        # Poll for result
        check_url = f"https://stablehorde.net/api/v2/generate/check/{request_id}"
        max_wait = 90
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            check_response = requests.get(check_url, timeout=10)
            if check_response.status_code == 200:
                check_data = check_response.json()
                
                if check_data.get("done"):
                    print("✅ Generation complete!")
                    status_url = f"https://stablehorde.net/api/v2/generate/status/{request_id}"
                    status_response = requests.get(status_url, timeout=10)
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        generations = status_data.get("generations", [])
                        
                        if generations and len(generations) > 0:
                            image_url = generations[0].get("img")
                            if image_url:
                                img_response = requests.get(image_url, timeout=30)
                                if img_response.status_code == 200:
                                    image_bytes = img_response.content
                                    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                                    return f"data:image/jpeg;base64,{image_base64}"
                    
                    raise Exception("Could not retrieve generated image")
                
                wait_time = check_data.get("wait_time", 5)
                time.sleep(min(wait_time, 5))
            else:
                time.sleep(3)
        
        raise Exception("Generation timed out after 90 seconds")
            
    except Exception as e:
        print(f"❌ Stable Horde error: {str(e)}")
        raise Exception(f"Stable Horde error: {str(e)}")

def generate_with_wan25(prompt, seed=None):
    """Generate using Turbo model via Pollinations - Completely FREE! Uses full prompts"""
    try:
        # Use turbo model (fast and high quality)
        # USE FULL PROMPT like server.py
        encoded_prompt = quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        # Add seed for variation
        if seed is None:
            seed = random.randint(1, 999999)
        
        print(f"Generating with Turbo AI (seed: {seed})...")
        print(f"Full Prompt: {prompt[:100]}...")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            # Convert to base64
            image_bytes = response.content
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            print("✅ Success with full prompt!")
            return f"data:image/jpeg;base64,{image_base64}"
        else:
            raise Exception(f"HTTP {response.status_code}")
            
    except Exception as e:
        raise Exception(f"Generation error: {str(e)}")

def generate_logo_data(company_name, industry=None, style=None, color_scheme=None):
    """Generate SVG logo design data"""
    
    if not style or style not in LOGO_STYLES:
        style = random.choice(LOGO_STYLES)
    
    colors = COLOR_SCHEMES.get(color_scheme) if color_scheme else None
    if not colors:
        base_hue = random.random()
        colors = []
        for i in range(3):
            hue = (base_hue + i * 0.33) % 1.0
            saturation = random.uniform(0.5, 0.9)
            lightness = random.uniform(0.4, 0.7)
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
            )
            colors.append(hex_color)
    
    initials = ''.join([word[0].upper() for word in company_name.split()[:2]])
    if len(initials) == 0:
        initials = company_name[:2].upper()
    
    shape = random.choice(['circle', 'square', 'triangle', 'hexagon', 'diamond', 'star'])
    
    return {
        'company_name': company_name,
        'initials': initials,
        'style': style,
        'colors': colors,
        'primary_color': colors[0],
        'secondary_color': colors[1],
        'accent_color': colors[2],
        'shape': shape,
        'font_style': random.choice(['modern', 'classic', 'bold', 'elegant', 'playful']),
        'layout': random.choice(['horizontal', 'vertical', 'stacked']),
        'has_icon': style not in ['wordmark'],
        'has_background': random.choice([True, False]),
        'border_radius': random.randint(0, 20),
        'rotation': random.randint(-15, 15) if style == 'abstract' else 0,
        'type': 'svg'
    }

@app.route('/')
def index():
    """Render the main page"""
    try:
        return render_template('index_modern.html')
    except Exception as e:
        print(f"Error loading template: {e}")
        return f"Error: {e}", 500

@app.route('/generate', methods=['POST'])
def generate():
    """Generate SVG logos"""
    data = request.json
    company_name = data.get('company_name', 'Company')
    industry = data.get('industry')
    style = data.get('style')
    color_scheme = data.get('color_scheme')
    count = int(data.get('count', 6))
    
    logos = []
    for _ in range(count):
        logo_design = generate_logo_data(company_name, industry, style, color_scheme)
        logos.append(logo_design)
    
    return jsonify({'logos': logos, 'success': True})

@app.route('/generate-free-ai', methods=['POST'])
def generate_free_ai():
    """Generate FREE AI logos using Pollinations.AI or Wan 2.5"""
    data = request.json
    company_name = data.get('company_name', 'Company')
    industry = data.get('industry', '')
    style = data.get('style', 'minimal')
    color_scheme = data.get('color_scheme', 'professional')
    count = int(data.get('count', 3))
    model = data.get('model', 'pollinations')  # 'pollinations' or 'wan25'
    background = data.get('background', 'natural')  # background style
    
    # Rate limiting based on user plan
    ip_address = request.remote_addr
    user_email = session.get('user_email')
    
    # Get user's plan
    if user_email:
        user = db.get_user(user_email)
        tier = user['plan'] if user else 'free'
        daily_limit = user['daily_limit'] if user else 10
    else:
        # Not logged in - use IP-based anonymous tier (3 free images)
        tier = 'anonymous'
        daily_limit = 3
    
    # Check if user can generate
    if daily_limit != -1:  # -1 means unlimited
        can_generate, remaining = rate_limiter.check_limit(ip_address, user_id=user_email, tier=tier)
        
        if not can_generate:
            # Check if user is logged in
            if not user_email:
                # Not logged in - ask to sign up for 10 daily images
                return jsonify({
                    'success': False,
                    'error': 'Daily limit reached',
                    'message': 'You have used your 3 free trial images! Sign up for FREE to get 10 images daily!',
                    'limit_reached': True,
                    'need_signup': True,
                    'signup_url': '/signup'
                }), 429
            else:
                # Logged in - ask to upgrade
                return jsonify({
                    'success': False,
                    'error': 'Daily limit reached',
                    'message': f'You have reached your daily limit. Upgrade to generate more!',
                    'limit_reached': True,
                    'need_signup': False,
                    'upgrade_url': '/pricing'
                }), 429
    else:
        can_generate = True
        remaining = -1
    
    logos = []
    errors = []
    
    print(f"\n{'='*60}")
    print(f"Generating {count} FREE AI logos for: {company_name}")
    print(f"{'='*60}\n")
    
    for i in range(count):
        try:
            # Increment usage counter BEFORE generating (so limit check works correctly next time)
            rate_limiter.increment(ip_address, user_id=user_email)
            
            # Create prompt with variation and background style
            prompt = create_logo_prompt(company_name, style, industry, color_scheme, variation=i, background=background)
            
            # Generate unique seed for this logo
            seed = random.randint(1, 999999)
            
            print(f"Logo {i+1}/{count}:")
            print(f"Prompt: {prompt[:80]}...")
            
            # Generate based on selected model - ONLY pollinations and stable-horde
            if model == 'pollinations':
                try:
                    image_data = generate_with_pollinations(prompt, seed=seed, model='flux')
                    model_name = 'Numidia Creative'
                except Exception as poll_error:
                    # Pollinations failed - automatically fallback to Stable Horde
                    print(f"⚠️ Pollinations failed, trying Stable Horde as fallback...")
                    image_data = generate_with_stable_horde(prompt, seed=seed)
                    model_name = 'Numidia Imagine (Auto-Fallback)'
            elif model == 'stable-horde':
                image_data = generate_with_stable_horde(prompt, seed=seed)
                model_name = 'Numidia Imagine'
            else:
                # Default to stable-horde for reliability
                image_data = generate_with_stable_horde(prompt, seed=seed)
                model_name = 'Numidia Imagine'
            
            if image_data:
                
                logos.append({
                    'url': image_data,
                    'prompt': prompt,
                    'style': style,
                    'color_scheme': color_scheme,
                    'company_name': company_name,
                    'type': 'ai',
                    'provider': model,
                    'model': f'{model_name} (FREE)',
                    'timestamp': datetime.now().isoformat()
                })
                print(f"✅ Logo {i+1} completed!\n")
            else:
                errors.append(f"Failed to generate logo {i+1}")
                print(f"❌ Logo {i+1} failed\n")
                
        except Exception as e:
            error_msg = str(e)
            errors.append(f"Error generating logo {i+1}: {error_msg}")
            print(f"❌ Error: {error_msg}\n")
    
    if not logos:
        # Create a user-friendly error message based on the model used
        selected_model = data.get('model', 'pollinations')
        if selected_model == 'pollinations':
            error_message = '⏱️ Numidia Creative is currently experiencing high demand. Please switch to Numidia Imagine (🌙) for instant results!'
        elif selected_model == 'stable-horde':
            error_message = '⚠️ Generation failed. Please try again or adjust your prompt.'
        else:
            error_message = 'Failed to generate images. Please try again with a different model.'
        
        return jsonify({
            'success': False,
            'error': error_message,
            'details': errors
        }), 500
    
    print(f"{'='*60}")
    print(f"✅ Successfully generated {len(logos)} logos!")
    print(f"{'='*60}\n")
    
    if model == 'pollinations':
        model_name = 'Numidia Creative'
    elif model == 'stable-horde':
        model_name = 'Numidia Imagine'
    else:
        model_name = 'Numidia Creative'
    
    return jsonify({
        'success': True,
        'logos': logos,
        'errors': errors if errors else None,
        'message': f'Generated {len(logos)} FREE AI logos using {model_name}'
    })

@app.route('/api/models')
def api_models():
    """Get available free AI services"""
    return jsonify({
        'models': FREE_AI_SERVICES,
        'recommended': 'pollinations'
    })

@app.route('/api/status')
def api_status():
    """Check system status"""
    return jsonify({
        'svg_generator': True,
        'free_ai': True,
        'service': 'Pollinations.AI',
        'api_key_needed': False,
        'cost': '$0'
    })

@app.route('/color-schemes')
def get_color_schemes():
    """Get available color schemes"""
    return jsonify({'schemes': COLOR_SCHEMES})

@app.route('/styles')
def get_styles():
    """Get available logo styles"""
    return jsonify({'styles': LOGO_STYLES})

@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    """Terms of Service page"""
    return render_template('terms.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/faq')
def faq():
    """FAQ page"""
    return render_template('faq.html')

@app.route('/pricing')
def pricing():
    """Pricing page - let everyone view it"""
    return render_template('pricing.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create PayPal payment"""
    plan_type = request.form.get('price_id')
    plan = PLANS.get(plan_type)
    
    if not plan:
        return "Invalid plan", 400
    
    # Render PayPal button page
    return render_template('paypal_checkout.html', 
                         plan=plan, 
                         plan_type=plan_type,
                         paypal_email=PAYPAL_BUSINESS_EMAIL)

@app.route('/success')
def success():
    """Payment success page"""
    session_id = request.args.get('session_id')
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Successful - Numidia AI</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            .success-box {{
                background: #2a2a2a;
                padding: 60px;
                border-radius: 20px;
                text-align: center;
                max-width: 500px;
            }}
            h1 {{ font-size: 48px; margin: 0 0 20px 0; }}
            p {{ font-size: 18px; color: #aaa; margin: 20px 0; }}
            a {{
                display: inline-block;
                background: linear-gradient(135deg, #e0e7ff 0%, #f8fafc 100%);
                color: #1e293b;
                padding: 15px 40px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: 700;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="success-box">
            <h1>✅ Payment Successful!</h1>
            <p>Thank you for subscribing to Numidia AI!</p>
            <p>Your account has been upgraded.</p>
            <a href="/">Start Creating →</a>
        </div>
    </body>
    </html>
    """

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        
        if password != confirm:
            return render_template('signup.html', error='Passwords do not match')
        
        success, message = db.create_user(email, password)
        if success:
            session['user_email'] = email
            return redirect('/')
        else:
            return render_template('signup.html', error=message)
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if db.verify_user(email, password):
            session['user_email'] = email
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user_email', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_email' not in session:
        return redirect('/login')
    
    user = db.get_user(session['user_email'])
    usage = rate_limiter.get_usage(request.remote_addr, session['user_email'])
    
    return render_template('dashboard.html', user=user, usage=usage)

@app.route('/paypal-success', methods=['GET', 'POST'])
def paypal_success():
    """Handle PayPal success"""
    plan_type = request.args.get('plan', 'basic')
    
    # Update user's plan if logged in
    if 'user_email' in session:
        db.update_plan(session['user_email'], plan_type)
        print(f"User {session['user_email']} upgraded to {plan_type}")
    
    return redirect('/success?plan=' + plan_type)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/blog')
def blog():
    """Blog and resources page"""
    return render_template('blog.html')

@app.route('/examples')
def examples():
    """Examples and inspiration page"""
    return render_template('examples.html')

@app.route('/guide')
def guide():
    """Complete guide page"""
    return render_template('guide.html')

@app.route('/ads.txt')
def ads_txt():
    """Serve ads.txt file for Ezoic"""
    from flask import Response
    # Ezoic ads.txt - Replace with your actual publisher ID from Ezoic dashboard
    ads_content = """# Ezoic Ads.txt
# Once you get your publisher ID from Ezoic dashboard, replace the line below
ezoic.com, pub-ezoicinccom, DIRECT
ezoic.com, pub-ezoicinccom, RESELLER
google.com, pub-9840848405074564, RESELLER, f08c47fec0942fa0
"""
    return Response(ads_content, mimetype='text/plain')

if __name__ == '__main__':
    import os
    
    # Get port from environment variable (for deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Check if running in production
    is_production = os.environ.get('RENDER') or os.environ.get('RAILWAY_ENVIRONMENT')
    
    if not is_production:
        print("\n" + "="*60)
        print("🎨 AI Image Generator")
        print("="*60)
        print("\n✨ Features:")
        print("  • FREE AI Image Generation")
        print("  • 3 AI Models Available")
        print("  • No API Key Needed")
        print("  • Completely FREE!")
        print("\n" + "="*60)
        print(f"🚀 Starting server on http://localhost:{port}")
        print("="*60 + "\n")
    
    app.run(debug=not is_production, host='0.0.0.0', port=port)
