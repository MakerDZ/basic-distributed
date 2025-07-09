import time
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get callback URL from environment (optional)
CALLBACK_URL = os.getenv('CALLBACK_URL')

def notify_completion(video_path: str, result: str):
    """Notify external service about job completion"""
    if not CALLBACK_URL:
        print("No callback URL configured, skipping notification")
        return
        
    try:
        response = requests.post(CALLBACK_URL, 
            json={
                "status": "completed",
                "video_path": video_path,
                "result_path": result,
                "timestamp": time.time()
            }
        )
        print(f"Notification sent, status: {response.status_code}")
    except Exception as e:
        print(f"Failed to send completion notification: {e}")

def process_video(video_path: str):
    print(f"Processing {video_path} ...")
    time.sleep(10)  # simulate heavy task
    result = f"{video_path}_processed.mp4"  # mock result
    print(f"Done processing {video_path}")
    
    # Send completion notification
    notify_completion(video_path, result)
    
    return result
