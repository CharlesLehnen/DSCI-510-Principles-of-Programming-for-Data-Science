from urllib.parse import urlparse
import multiprocessing
import capture_images
import signal
import os
import subprocess

def download_video(url):
    # Set up folder and file structure
    video_folder = os.path.join("data", "videos")
    if not os.path.exists(video_folder):
        os.mkdir(video_folder)
    parsed_url = urlparse(url)
    video_id = parsed_url.query.split("&")[0].split("=")[1]

    # Download video
    video_output = os.path.join(os.getcwd(), "data", "videos")
    command = [
        "youtube-dl",
        "--output", f"{video_output}/video_%(id)s.%(ext)s", # This fixed the default naming conflict errors
        "--no-part", # This fixed the .mp4.part issue
        url
    ]

    youtube_dl_process = subprocess.Popen(command) # Subprocess seems to be the only way to get it to run
        
    # Capture images from video simultaneously using capture_images.py
    image_capture_process = multiprocessing.Process(
        target=capture_images.capture_images,
        args=(video_id,)
    )
    image_capture_process.start()
    

if __name__ == "__main__":
    # Set the URL of the YouTube live video and run
    url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
    download_process = multiprocessing.Process(target=download_video, args=(url,))
    download_process.start()