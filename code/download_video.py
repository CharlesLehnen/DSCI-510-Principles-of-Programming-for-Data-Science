from urllib.parse import urlparse
import multiprocessing
import signal
import os
import subprocess
import time
import os
import cv2
from PIL import Image
import capture_images

def download_video(*urls):
    # Set up folder and file structure
    video_folder = os.path.join("data", "videos")
    if not os.path.exists(video_folder):
        os.mkdir(video_folder)

    # Download videos in parallel
    youtube_dl_processes = []
    for url in urls:
        # Download video
        video_output = os.path.join(os.getcwd(), "data", "videos")
        command = [
            "youtube-dl",
            "--verbose",
            "--output", f"{video_output}/video_%(id)s.%(ext)s", # This fixed the default naming conflict errors
            "--no-part", # This fixed the .mp4.part issue
            url
        ]
        youtube_dl_process = multiprocessing.Process(target=subprocess.run, args=(command,))
        youtube_dl_process.start()
        youtube_dl_processes.append(youtube_dl_process)
        
    # Capture images from videos simultaneously using capture_images.py
    for url, youtube_dl_process in zip(urls, youtube_dl_processes):
        parsed_url = urlparse(url)
        video_id = parsed_url.query.split("&")[0].split("=")[1]
        image_capture_process = multiprocessing.Process(
            target=capture_images.capture_images,
            args=(video_id,)
        )
        image_capture_process.start()


def signal_handler(signal, frame):
    for youtube_dl_process in youtube_dl_processes:
        youtube_dl_process.terminate()
    sys.exit(0)

if __name__ == "__main__":
    # Set the URLs of the YouTube live videos and run
    urls = ["https://www.youtube.com/watch?v=ydYDqZQpim8", "https://www.youtube.com/watch?v=gUZjDCZEMDA"]
    # Original link does not work right now: "https://www.youtube.com/watch?v=UeB6UcZpUzk"
    download_process = multiprocessing.Process(target=download_video, args=urls)
    download_process.start()

    # Register signal handler to terminate youtube-dl processes gracefully
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
