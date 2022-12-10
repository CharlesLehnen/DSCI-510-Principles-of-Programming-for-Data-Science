from urllib.parse import urlparse
import multiprocessing
import signal
import os
import subprocess
import time
import os
import cv2
from PIL import Image


url = "https://www.youtube.com/watch?v=48MFrf5ADp8"


def capture_images(video_id, capture_interval = 120):
    # Capture images from the video
    try:
        # Set the output and image folders
        video_output = os.path.join(os.getcwd(), "data", "videos")
        image_folder = os.path.join("data", "images")
        if not os.path.exists(image_folder):
            os.mkdir(image_folder)

        # Open the video file
        vidcap = cv2.VideoCapture(os.path.join(video_output, f"video_{video_id}.mp4"))

        # Capture images
        success, image = vidcap.read()
        image_number = 1
        
        while success:
            image_number += 1
            image_file = os.path.join(image_folder, f"image_{video_id}_{image_number}.jpg")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            Image.fromarray(image).save(image_file)
            time.sleep(capture_interval)  # Sleep for the specified capture interval
            success, image = vidcap.read()

    except KeyboardInterrupt:
        # Kill the youtube-dl process
        youtube_dl_process.terminate()
        download_process.terminate()


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
    


