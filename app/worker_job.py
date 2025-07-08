import time

def process_video(video_path: str):
    print(f"Processing {video_path} ...")
    time.sleep(10)  # simulate heavy task
    result = f"{video_path}_processed.mp4"  # mock result
    print(f"Done processing {video_path}")
    return result
