#!/usr/bin/env python3
"""
TikTok Auto-Poster for Unlimagen
Generates AI images and posts to TikTok every 10 minutes
"""

import requests
import time
import random
from datetime import datetime

# ===== CONFIGURATION =====
UNLIMAGEN_URL = "https://unlimagen.com"  # Your website URL
TIKTOK_ACCESS_TOKEN = "YOUR_TIKTOK_ACCESS_TOKEN"  # Get from TikTok Developer Portal
VERIFIED_DOMAIN = "https://unlimagen.com"  # Your verified domain for hosting images

# Image generation prompts
PROMPTS = [
    "A futuristic city at sunset, digital art",
    "Abstract colorful pattern, vibrant colors",
    "Cute robot character, 3D render",
    "Beautiful landscape with mountains",
    "Modern minimalist logo design",
    "Cyberpunk neon street scene",
    "Fantasy castle in the clouds",
    "Ocean waves at golden hour",
    "Space galaxy with stars",
    "Geometric abstract art"
]

# TikTok captions
CAPTIONS = [
    "AI generated art! 🎨 Follow for more #AIart #generativeart",
    "Created with AI in seconds! ✨ #artificialintelligence #digitalart",
    "What do you think? 🤔 #aiartwork #creativity",
    "Free AI image generator at unlimagen.com 🚀 #aitools #art",
    "Made with artificial intelligence 🤖 #aiart #design"
]

# Image types available on Unlimagen
IMAGE_TYPES = [
    "Logo", "Photorealistic", "Digital Art", "Painting",
    "Sketch", "3D Render", "Abstract", "Minimalist"
]

# ===== FUNCTIONS =====

def generate_image_on_unlimagen():
    """
    Generates an AI image using Unlimagen website
    Returns: Image URL or file path
    """
    try:
        # Select random prompt and type
        prompt = random.choice(PROMPTS)
        image_type = random.choice(IMAGE_TYPES)
        
        print(f"🎨 Generating image: {prompt} ({image_type})")
        
        # Make request to Unlimagen API
        # Note: You'll need to add an API endpoint to your Flask app
        response = requests.post(
            f"{UNLIMAGEN_URL}/api/generate",  # Create this endpoint
            json={
                "prompt": prompt,
                "image_type": image_type,
                "model": "miragic"  # or "turbo" or "creative"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            image_url = data.get("image_url")
            print(f"✅ Image generated: {image_url}")
            return image_url
        else:
            print(f"❌ Error generating image: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def download_image(image_url):
    """
    Downloads image from URL to local file
    Returns: Local file path
    """
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            filename = f"ai_image_{int(time.time())}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"📥 Image downloaded: {filename}")
            return filename
        return None
    except Exception as e:
        print(f"❌ Download error: {e}")
        return None


def post_photo_to_tiktok(image_url, caption):
    """
    Posts photo to TikTok using Content Posting API
    TikTok supports photo posts (carousels)
    """
    try:
        print(f"📤 Posting photo to TikTok...")
        
        headers = {
            "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Initialize photo upload
        response = requests.post(
            "https://open.tiktokapis.com/v2/post/publish/content/init/",
            headers=headers,
            json={
                "post_info": {
                    "title": caption[:150],  # Max 150 chars
                    "description": caption,
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                    "disable_duet": False,
                    "disable_comment": False,
                    "disable_stitch": False
                },
                "source_info": {
                    "source": "PULL_FROM_URL",
                    "photo_cover_index": 1,
                    "photo_images": [image_url]  # Single image
                },
                "post_mode": "DIRECT_POST",  # or "MEDIA_UPLOAD" for draft
                "media_type": "PHOTO"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('error', {}).get('code') == 'ok':
                publish_id = data['data']['publish_id']
                print(f"✅ Photo posted to TikTok! Publish ID: {publish_id}")
                return True
            else:
                print(f"❌ TikTok API error: {data.get('error', {})}")
                return False
        else:
            print(f"❌ TikTok API error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ TikTok posting error: {e}")
        return False


def post_video_to_tiktok(video_path, caption):
    """
    Posts video to TikTok using FILE_UPLOAD method
    """
    try:
        import os
        
        print(f"📤 Posting video to TikTok...")
        
        headers = {
            "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Get video file size
        video_size = os.path.getsize(video_path)
        
        # Step 1: Initialize upload
        init_response = requests.post(
            "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/",
            headers=headers,
            json={
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": video_size,
                    "chunk_size": video_size,
                    "total_chunk_count": 1
                }
            }
        )
        
        if init_response.status_code != 200:
            print(f"❌ Init failed: {init_response.status_code}")
            print(init_response.text)
            return False
        
        data = init_response.json()
        if data.get('error', {}).get('code') != 'ok':
            print(f"❌ Init error: {data.get('error', {})}")
            return False
        
        publish_id = data['data']['publish_id']
        upload_url = data['data']['upload_url']
        
        print(f"📤 Uploading video... (Publish ID: {publish_id})")
        
        # Step 2: Upload video file
        with open(video_path, 'rb') as video_file:
            video_data = video_file.read()
            
        upload_headers = {
            'Content-Range': f'bytes 0-{video_size-1}/{video_size}',
            'Content-Type': 'video/mp4'
        }
        
        upload_response = requests.put(
            upload_url,
            headers=upload_headers,
            data=video_data
        )
        
        if upload_response.status_code in [200, 201, 204]:
            print(f"✅ Video uploaded! User will see in TikTok inbox")
            print(f"📱 User must review and post from TikTok app")
            return True
        else:
            print(f"❌ Upload failed: {upload_response.status_code}")
            print(upload_response.text)
            return False
            
    except Exception as e:
        print(f"❌ TikTok posting error: {e}")
        return False


def convert_image_to_video(image_path):
    """
    Converts static image to video (required for TikTok)
    Requires ffmpeg installed
    """
    try:
        import subprocess
        
        output_video = f"video_{int(time.time())}.mp4"
        
        # Create 5-second video from image using ffmpeg
        command = [
            'ffmpeg',
            '-loop', '1',
            '-i', image_path,
            '-c:v', 'libx264',
            '-t', '5',
            '-pix_fmt', 'yuv420p',
            '-vf', 'scale=1080:1920',  # TikTok vertical format
            output_video
        ]
        
        subprocess.run(command, check=True, capture_output=True)
        print(f"🎬 Video created: {output_video}")
        return output_video
        
    except Exception as e:
        print(f"❌ Video conversion error: {e}")
        return None


def auto_post_loop():
    """
    Main loop: Generate and post every 10 minutes
    """
    print("🚀 TikTok Auto-Poster Started!")
    print(f"⏰ Posting every 10 minutes")
    print(f"🌐 Using: {UNLIMAGEN_URL}")
    print("-" * 50)
    
    post_count = 0
    
    while True:
        try:
            post_count += 1
            print(f"\n📍 Post #{post_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Step 1: Generate image
            image_url = generate_image_on_unlimagen()
            
            if image_url:
                # Step 2: Download image
                image_path = download_image(image_url)
                
                if image_path:
                    # Option 1: Post as photo (easier, no video conversion needed)
                    caption = random.choice(CAPTIONS)
                    success = post_photo_to_tiktok(image_url, caption)
                    
                    if success:
                        print(f"✅ Successfully posted photo #{post_count}!")
                    else:
                        print(f"⚠️  Photo post failed, trying video method...")
                        
                        # Option 2: Convert to video and post (fallback)
                        video_path = convert_image_to_video(image_path)
                        
                        if video_path:
                            success = post_video_to_tiktok(video_path, caption)
                            
                            if success:
                                print(f"✅ Successfully posted video #{post_count}!")
                            else:
                                print(f"❌ Failed to post #{post_count}")
                        else:
                            print("❌ Video conversion failed")
                else:
                    print("❌ Image download failed")
            else:
                print("❌ Image generation failed")
            
            # Wait 10 minutes (600 seconds)
            print(f"\n⏳ Waiting 10 minutes until next post...")
            time.sleep(600)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Stopped by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("⏳ Waiting 10 minutes before retry...")
            time.sleep(600)


# ===== MAIN =====
if __name__ == "__main__":
    # Check if TikTok token is configured
    if TIKTOK_ACCESS_TOKEN == "YOUR_TIKTOK_ACCESS_TOKEN":
        print("⚠️  WARNING: TikTok access token not configured!")
        print("Please follow the setup instructions in TIKTOK_SETUP.md")
        print("\nRunning in TEST MODE (no actual TikTok posting)")
        print("-" * 50)
    
    auto_post_loop()
