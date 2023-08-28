from urllib.parse import urlparse
import multiprocessing
import signal
import os
import subprocess
import time
import os
import cv2
from PIL import Image

def download_video(url):
    try :
        # Print current working directory for debugging
        print(f"Current working directory: {os.getcwd()}")

        # Set up folder and file structure using absolute paths
        base_dir = os.path.abspath(os.getcwd())
        data_folder = os.path.join(base_dir, "data")
        video_folder = os.path.join(data_folder, "videos")

        # Print paths for debugging
        print(f"Data folder: {data_folder}")
        print(f"Video folder: {video_folder}")

        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        
        if not os.path.exists(video_folder):
            os.mkdir(video_folder)

        # Download video
        video_output = os.path.join(os.getcwd(), "data", "videos")
        command = [
            "youtube-dl",
            "--verbose",
            "--output", f"{video_output}/video_%(id)s.%(ext)s", # This fixed the default naming conflict errors
            "--no-part", # This fixed the .mp4.part issue
            url
        ]
        subprocess.run(command)
        
    # This is the only way to accomplish this! I tried everything
    except KeyboardInterrupt:
        # Kill the youtube-dl process
        youtube_dl_process.terminate()
        download_process.terminate()

    
if __name__ == "__main__":
    # Set the URLs of the YouTube live videos and run
    urls = ["https://www.youtube.com/watch?v=ydYDqZQpim8", "https://www.youtube.com/watch?v=gUZjDCZEMDA"]
    # Original link does not work right now: "https://www.youtube.com/watch?v=UeB6UcZpUzk"
    
    # Run function
    with multiprocessing.Pool() as pool:
        pool.map(download_video, urls)
