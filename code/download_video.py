from urllib.parse import urlparse
import multiprocessing
import signal
import os
import subprocess
import time
import os
import cv2
from PIL import Image
import platform

def download_video(url):

    # Add youtube-dl to system PATH
    ## Determine the operating system
    os_type = platform.system()

    ## Get the path to youtube-dl based on the operating system
    if os_type == "Windows":
        try:
            youtube_dl_path = subprocess.check_output(["where", "youtube-dl"], text=True).strip()
        except subprocess.CalledProcessError:
            print("youtube-dl not found. Please install it.")
            exit(1)
    else:  # For Linux and macOS
        try:
            youtube_dl_path = subprocess.check_output(["which", "youtube-dl"], text=True).strip()
        except subprocess.CalledProcessError:
            print("youtube-dl not found. Please install it.")
    ## Add the directory containing youtube-dl to the PATH
    os.environ["PATH"] += os.pathsep + os.path.dirname(youtube_dl_path)

    # Download video
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
