#!/usr/bin/env python3
"""
Advanced TikTok Video Automation
- Generates trending motivational videos
- Multiple AI images per video
- AI voiceover
- Auto-posts to TikTok
"""

import requests
import random
import time
import json
from datetime import datetime
import os

# ===== CONFIGURATION =====
UNLIMAGEN_URL = "https://unlimagen.com"
TIKTOK_ACCESS_TOKEN = "YOUR_TIKTOK_ACCESS_TOKEN"

# API Keys (Get these from respective services)
ELEVENLABS_API_KEY = "YOUR_ELEVENLABS_API_KEY"  # For AI voice
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"  # For trending topics & scripts

# ===== TRENDING TOPICS =====
def get_trending_topics():
    """
    Get trending topics using AI or predefined categories
    """
    # Predefined trending categories
    categories = [
        "AI Technology",
        "Self Improvement",
        "Productivity Hacks",
        "Mental Health",
        "Success Mindset",
        "Fitness Motivation",
        "Business Growth",
        "Cryptocurrency",
        "Social Media Tips",
        "Life Lessons",
        "Morning Routines",
        "Time Management",
        "Passive Income",
        "Study Tips",
        "Healthy Habits"
    ]
    
    # You can also fetch from trending APIs
    # For now, return random category
    return random.choice(categories)


def generate_video_script(topic):
    """
    Generate 30-second video script using AI
    """
    
    # Option 1: Use OpenAI GPT (Recommended)
    if OPENAI_API_KEY != "YOUR_OPENAI_API_KEY":
        try:
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            prompt = f"""Create a 30-second TikTok video script about {topic}.

Requirements:
- Hook in first 3 seconds
- 3-4 main points
- Conversational, engaging tone
- End with call to action
- Include timestamps
- Total: ~75-90 words

Format:
[0-3s] Hook
[3-10s] Point 1
[10-18s] Point 2
[18-25s] Point 3
[25-30s] CTA
"""
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a viral TikTok content creator."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 200
                },
                timeout=30
            )
            
            if response.status_code == 200:
                script = response.json()["choices"][0]["message"]["content"]
                print(f"✅ Generated script with AI")
                return parse_script(script)
            
        except Exception as e:
            print(f"⚠️  OpenAI error: {e}")
    
    # Option 2: Predefined templates
    return generate_template_script(topic)


def generate_template_script(topic):
    """
    Generate script from templates
    """
    templates = {
        "AI Technology": {
            "hook": "Did you know AI can now do THIS?",
            "points": [
                "AI can generate photorealistic images in seconds",
                "It can write code, music, and even entire videos",
                "The future is here and it's accessible to everyone"
            ],
            "cta": "Try it yourself at Unlimagen.com - 100% free!"
        },
        "Self Improvement": {
            "hook": "Want to change your life? Start here.",
            "points": [
                "Small daily habits create massive results",
                "Consistency beats perfection every single time",
                "You're one decision away from a different life"
            ],
            "cta": "Follow for more motivation! Drop a ❤️"
        },
        "Productivity Hacks": {
            "hook": "This productivity hack changed my life.",
            "points": [
                "Use the 2-minute rule for small tasks",
                "Time-block your calendar for deep work",
                "Eliminate distractions for 90-minute sprints"
            ],
            "cta": "Save this and try it tomorrow!"
        },
        "Success Mindset": {
            "hook": "Successful people think differently.",
            "points": [
                "They focus on solutions, not problems",
                "They invest in themselves first",
                "They take action despite fear"
            ],
            "cta": "Which one resonates with you? Comment below!"
        }
    }
    
    # Get template or use default
    template = templates.get(topic, templates["Self Improvement"])
    
    script = {
        "topic": topic,
        "segments": [
            {"time": "0-3", "text": template["hook"], "image_prompt": f"{topic} inspiring visual"},
            {"time": "3-12", "text": template["points"][0], "image_prompt": f"{template['points'][0]} visualization"},
            {"time": "12-21", "text": template["points"][1], "image_prompt": f"{template['points'][1]} concept art"},
            {"time": "21-27", "text": template["points"][2], "image_prompt": f"{template['points'][2]} digital art"},
            {"time": "27-30", "text": template["cta"], "image_prompt": f"{topic} call to action"}
        ]
    }
    
    return script


def parse_script(script_text):
    """
    Parse AI-generated script into structured format
    """
    lines = script_text.strip().split('\n')
    segments = []
    
    for line in lines:
        if '[' in line and ']' in line:
            time_range = line[line.find('[')+1:line.find(']')]
            text = line[line.find(']')+1:].strip()
            
            if text:
                segments.append({
                    "time": time_range,
                    "text": text,
                    "image_prompt": f"{text[:50]} visual representation"
                })
    
    if len(segments) < 3:
        # Fallback to template
        return generate_template_script("Motivation")
    
    return {"segments": segments}


def generate_images_for_script(script):
    """
    Generate AI images for each segment
    """
    images = []
    
    for i, segment in enumerate(script["segments"]):
        print(f"🎨 Generating image {i+1}/{len(script['segments'])}: {segment['text'][:50]}...")
        
        # Use Unlimagen API
        try:
            response = requests.post(
                f"{UNLIMAGEN_URL}/api/generate",
                json={
                    "prompt": segment["image_prompt"],
                    "image_type": "Digital Art",
                    "model": "miragic"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                image_url = data.get("image_url")
                
                # Download image
                img_response = requests.get(image_url, timeout=10)
                if img_response.status_code == 200:
                    filename = f"segment_{i}_{int(time.time())}.png"
                    with open(filename, 'wb') as f:
                        f.write(img_response.content)
                    
                    images.append({
                        "filename": filename,
                        "text": segment["text"],
                        "time": segment["time"]
                    })
                    print(f"✅ Image {i+1} generated")
                else:
                    print(f"❌ Failed to download image {i+1}")
            
        except Exception as e:
            print(f"❌ Error generating image {i+1}: {e}")
        
        # Avoid rate limiting
        time.sleep(2)
    
    return images


def generate_voiceover(script):
    """
    Generate AI voiceover using ElevenLabs
    """
    print("🎙️ Generating voiceover...")
    
    # Combine all text
    full_text = " ... ".join([seg["text"] for seg in script["segments"]])
    
    if ELEVENLABS_API_KEY == "YOUR_ELEVENLABS_API_KEY":
        print("⚠️  ElevenLabs API key not set, skipping voiceover")
        return None
    
    try:
        # ElevenLabs API
        voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default voice (Rachel)
        
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers=headers,
            json={
                "text": full_text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            audio_filename = f"voiceover_{int(time.time())}.mp3"
            with open(audio_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Voiceover generated: {audio_filename}")
            return audio_filename
        else:
            print(f"❌ Voiceover API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Voiceover error: {e}")
        return None


def create_video_from_images(images, audio_file, output_filename):
    """
    Create 30-second video with images and audio using ffmpeg
    """
    print("🎬 Creating video...")
    
    try:
        import subprocess
        
        # Calculate duration per image (distribute 30 seconds)
        duration_per_image = 30 / len(images)
        
        # Create concat file for ffmpeg
        concat_filename = f"concat_{int(time.time())}.txt"
        with open(concat_filename, 'w') as f:
            for img in images:
                f.write(f"file '{img['filename']}'\n")
                f.write(f"duration {duration_per_image}\n")
            # Repeat last image to avoid early cut
            f.write(f"file '{images[-1]['filename']}'\n")
        
        # Build ffmpeg command
        command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_filename,
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-t', '30'
        ]
        
        # Add audio if available
        if audio_file and os.path.exists(audio_file):
            command.extend([
                '-i', audio_file,
                '-c:a', 'aac',
                '-shortest'
            ])
        
        command.append(output_filename)
        
        # Run ffmpeg
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Video created: {output_filename}")
            
            # Cleanup
            os.remove(concat_filename)
            for img in images:
                if os.path.exists(img['filename']):
                    os.remove(img['filename'])
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)
            
            return output_filename
        else:
            print(f"❌ FFmpeg error: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Video creation error: {e}")
        return None


def post_video_to_tiktok(video_file, caption):
    """
    Upload video to TikTok
    """
    print("📤 Uploading to TikTok...")
    
    if TIKTOK_ACCESS_TOKEN == "YOUR_TIKTOK_ACCESS_TOKEN":
        print("⚠️  TikTok token not configured")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        video_size = os.path.getsize(video_file)
        
        # Initialize upload
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
            print(f"❌ Init failed: {init_response.text}")
            return False
        
        data = init_response.json()
        publish_id = data['data']['publish_id']
        upload_url = data['data']['upload_url']
        
        # Upload video
        with open(video_file, 'rb') as f:
            video_data = f.read()
        
        upload_response = requests.put(
            upload_url,
            headers={
                'Content-Range': f'bytes 0-{video_size-1}/{video_size}',
                'Content-Type': 'video/mp4'
            },
            data=video_data
        )
        
        if upload_response.status_code in [200, 201, 204]:
            print(f"✅ Video uploaded! Publish ID: {publish_id}")
            print(f"📱 User will see notification in TikTok inbox")
            return True
        else:
            print(f"❌ Upload failed: {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ TikTok error: {e}")
        return False


def create_and_post_video():
    """
    Complete workflow: Generate video and post to TikTok
    """
    print("\n" + "="*50)
    print(f"🚀 Starting video creation - {datetime.now().strftime('%H:%M:%S')}")
    print("="*50)
    
    # Step 1: Get trending topic
    topic = get_trending_topics()
    print(f"📊 Topic: {topic}")
    
    # Step 2: Generate script
    print(f"📝 Generating script...")
    script = generate_video_script(topic)
    print(f"✅ Script created with {len(script['segments'])} segments")
    
    # Step 3: Generate images
    images = generate_images_for_script(script)
    
    if len(images) < 3:
        print("❌ Not enough images generated, skipping video")
        return False
    
    # Step 4: Generate voiceover
    audio_file = generate_voiceover(script)
    
    # Step 5: Create video
    video_filename = f"tiktok_video_{int(time.time())}.mp4"
    video_file = create_video_from_images(images, audio_file, video_filename)
    
    if not video_file:
        print("❌ Video creation failed")
        return False
    
    # Step 6: Post to TikTok
    caption = f"{topic} 💡✨ #motivation #ai #inspiration #fyp"
    success = post_video_to_tiktok(video_file, caption)
    
    # Cleanup
    if os.path.exists(video_file):
        os.remove(video_file)
    
    return success


def auto_post_loop(interval_hours=4):
    """
    Main loop: Create and post videos every X hours
    """
    print("🎥 TikTok Video Automation Started!")
    print(f"⏰ Creating videos every {interval_hours} hours")
    print(f"🌐 Using: {UNLIMAGEN_URL}")
    print("-" * 50)
    
    video_count = 0
    
    while True:
        try:
            video_count += 1
            print(f"\n📍 Video #{video_count}")
            
            success = create_and_post_video()
            
            if success:
                print(f"✅ Video #{video_count} posted successfully!")
            else:
                print(f"❌ Video #{video_count} failed")
            
            # Wait before next video
            wait_seconds = interval_hours * 3600
            print(f"\n⏳ Waiting {interval_hours} hours until next video...")
            time.sleep(wait_seconds)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Stopped by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print(f"⏳ Waiting {interval_hours} hours before retry...")
            time.sleep(interval_hours * 3600)


# ===== MAIN =====
if __name__ == "__main__":
    # Check configuration
    warnings = []
    
    if TIKTOK_ACCESS_TOKEN == "YOUR_TIKTOK_ACCESS_TOKEN":
        warnings.append("⚠️  TikTok access token not configured")
    
    if ELEVENLABS_API_KEY == "YOUR_ELEVENLABS_API_KEY":
        warnings.append("⚠️  ElevenLabs API key not set (videos will have no voice)")
    
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
        warnings.append("⚠️  OpenAI API key not set (using templates instead)")
    
    if warnings:
        print("\n".join(warnings))
        print("\nSee ADVANCED_SETUP.md for API keys")
        print("-" * 50)
    
    # Run automation (post every 4 hours - TikTok friendly)
    auto_post_loop(interval_hours=4)
