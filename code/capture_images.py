import time
import os
import cv2
from PIL import Image

def capture_images(video_id, capture_interval = 600):
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
