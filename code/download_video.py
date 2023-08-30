from urllib.parse import urlparse
import multiprocessing
import signal
import os
import subprocess
import time
import os
import cv2
from PIL import Image

def is_yt-dlp_installed():
    # Check if yt-dlp is installed.
    try:
        subprocess.check_output(["yt-dlp", "--version"], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def download_video(url):
    try :
         # Set up folder and file structure using absolute paths
        base_dir = os.path.abspath(os.getcwd())
        data_folder = os.path.join(base_dir, "data")
        video_folder = os.path.join(data_folder, "videos")

        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        
        if not os.path.exists(video_folder):
            os.mkdir(video_folder)

        # Download video
        video_output = os.path.join(os.getcwd(), "data", "videos")
        command = [
            "yt-dlp",
            "--print-traffic",
            "--verbose",
            "--output", f"{video_output}/video_%(id)s.%(ext)s", # This fixed the default naming conflict errors
            "--no-part", # This fixed the .mp4.part issue
            url
        ]
        subprocess.run(command)
        
    # This is the only way to accomplish this! I tried everything
    except KeyboardInterrupt:
        # Kill the youtube-dl process
        download_process.terminate()

    
if __name__ == "__main__":
    # Check if yt-dlp is installed
    if not is_yt-dlp_installed():
        print("Error: yt-dlp is not installed.")
        print("Please install it using: pip install yt-dlp")
        exit(1)
    
    # Set the URLs of the YouTube live videos and run
    urls = ["https://www.youtube.com/watch?v=ydYDqZQpim8", "https://www.youtube.com/watch?v=DsNtwGJXTTs"]
    # Original link does not work right now: "https://www.youtube.com/watch?v=UeB6UcZpUzk", "https://www.youtube.com/watch?v=gUZjDCZEMDA"
    
    # Run function
    with multiprocessing.Pool() as pool:
        pool.map(download_video, urls)
