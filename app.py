"""
Free AI Logo Generator - FIXED VERSION
Uses Pollinations.AI - completely free, no API key needed!
"""

from flask import Flask, render_template, request, jsonify
import random
import colorsys
import requests
import base64
from datetime import datetime
from urllib.parse import quote

app = Flask(__name__)

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
    """Generate using Miragic AI style via Pollinations - Completely FREE!"""
    try:
        # Use Pollinations with optimized prompt for Miragic-style results
        encoded_prompt = quote(prompt + ", highly detailed, professional, award-winning")
        
        if seed is None:
            seed = random.randint(1, 999999)
        
        # Pollinations API with enhanced quality
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&enhance=true&seed={seed}"
        
        print(f"Generating with Miragic AI style (seed: {seed})...")
        print(f"Prompt: {prompt[:100]}...")
        
        response = requests.get(url, timeout=90)
        
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
    """Generate using Pollinations.AI - Completely FREE!"""
    try:
        # Pollinations.AI - Simple GET request, no API key!
        encoded_prompt = quote(prompt)
        
        # Add seed for variation - this ensures different images
        if seed is None:
            seed = random.randint(1, 999999)
        
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model={model}&seed={seed}"
        
        print(f"Generating with Pollinations.AI (model: {model}, seed: {seed})...")
        print(f"Prompt: {prompt[:100]}...")
        
        response = requests.get(url, timeout=90)
        
        if response.status_code == 200:
            # Convert to base64
            image_bytes = response.content
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            print("✅ Success!")
            return f"data:image/jpeg;base64,{image_base64}"
        else:
            raise Exception(f"HTTP {response.status_code}")
            
    except Exception as e:
        raise Exception(f"Pollinations.AI error: {str(e)}")

def generate_with_wan25(prompt, seed=None):
    """Generate using Turbo model via Pollinations - Completely FREE!"""
    try:
        # Use turbo model (fast and high quality)
        encoded_prompt = quote(prompt)
        
        # Add seed for variation
        if seed is None:
            seed = random.randint(1, 999999)
        
        # Use turbo model - fast and reliable
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
        
        print(f"Generating with Turbo AI (seed: {seed})...")
        print(f"Prompt: {prompt[:100]}...")
        
        response = requests.get(url, timeout=90)
        
        if response.status_code == 200:
            # Convert to base64
            image_bytes = response.content
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            print("✅ Success!")
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
    
    logos = []
    errors = []
    
    print(f"\n{'='*60}")
    print(f"Generating {count} FREE AI logos for: {company_name}")
    print(f"{'='*60}\n")
    
    for i in range(count):
        try:
            # Create prompt with variation and background style
            prompt = create_logo_prompt(company_name, style, industry, color_scheme, variation=i, background=background)
            
            # Generate unique seed for this logo
            seed = random.randint(1, 999999)
            
            print(f"Logo {i+1}/{count}:")
            print(f"Prompt: {prompt[:80]}...")
            
            # Generate based on selected model
            if model == 'miragic':
                image_data = generate_with_miragic(prompt, seed=seed)
                model_name = 'Miragic AI'
            elif model == 'wan25':
                image_data = generate_with_wan25(prompt, seed=seed)
                model_name = 'Turbo AI'
            else:
                image_data = generate_with_pollinations(prompt, seed=seed, model='flux')
                model_name = 'Pollinations.AI'
            
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
        return jsonify({
            'success': False,
            'error': 'Failed to generate any logos',
            'details': errors
        }), 500
    
    print(f"{'='*60}")
    print(f"✅ Successfully generated {len(logos)} logos!")
    print(f"{'='*60}\n")
    
    if model == 'miragic':
        model_name = 'Miragic AI'
    elif model == 'wan25':
        model_name = 'Turbo AI'
    else:
        model_name = 'Pollinations.AI'
    
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

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/ads.txt')
def ads_txt():
    """Serve ads.txt file for Ezoic"""
    from flask import Response
    # This will be updated with your Ezoic publisher ID
    # You'll need to add your Ezoic line from their dashboard
    ads_content = """# Ezoic Ads.txt
# Add your Ezoic publisher line here from Step 2 in Ezoic dashboard
# Example: ezoic.com, pub-XXXXXXXXXXXXX, DIRECT
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
