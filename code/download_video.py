import os
import subprocess
from urllib.parse import urlparse
import multiprocessing
import capture_images
import signal

def download_video(url):
    # Set up folder and file structure
    video_folder = os.path.join("data", "videos")
    if not os.path.exists(video_folder):
        os.mkdir(video_folder)
    parsed_url = urlparse(url)
    video_id = parsed_url.query.split("&")[0].split("=")[1]

    # Download video
    video_output = os.path.join(os.getc_wd(), "data", "videos")
    command = [
        "youtube-dl",
        "--output", f"{video_output}/video_%(id)s.%(ext)s",
        "--no-part",
        url
    ]

    # Start the youtube_dl_process
    try:
        # Wait for the youtube_dl_process to finish
        youtube_dl_process.wait()
    finally:
        # Ensure that the youtube_dl_process is always terminated
        youtube_dl_process.terminate()
        
    # Capture images from the video
    image_capture_process = multiprocessing.Process(
        target=capture_images.capture_images,
        args=(video_id,)
    )
    image_capture_process.start()
