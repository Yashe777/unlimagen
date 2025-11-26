
import requests
import base64
import random
from urllib.parse import quote

def generate_with_pollinations(prompt, seed=None, model='turbo', width=512, height=512):
    """Generate using Pollinations.AI - Completely FREE!"""
    try:
        # Pollinations.AI - Simple GET request, no API key!
        encoded_prompt = quote(prompt)
        
        # Add seed for variation - this ensures different images
        if seed is None:
            seed = random.randint(1, 999999)
        
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model={model}&seed={seed}&width={width}&height={height}&nologo=true"
        
        print(f"Generating with Pollinations.AI (model: {model}, seed: {seed})...")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=60)
        
        if response.status_code == 200:
            # Convert to base64
            image_bytes = response.content
            print(f"Response content type: {response.headers.get('content-type')}")
            print(f"Response size: {len(image_bytes)} bytes")
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            print("✅ Success!")
            return f"data:image/jpeg;base64,{image_base64}"
        else:
            print(f"Failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            raise Exception(f"HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Exception: {e}")
        raise Exception(f"Pollinations.AI error: {str(e)}")

if __name__ == "__main__":
    print("Testing generation with Turbo (512x512)...")
    try:
        result = generate_with_pollinations("a futuristic city", seed=67890, model='turbo', width=512, height=512)
        print("Turbo generation successful.")
    except Exception as e:
        print(f"Turbo generation failed: {e}")
