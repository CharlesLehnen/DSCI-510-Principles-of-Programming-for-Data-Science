import time
import os
import cv2
from PIL import Image

def capture_images(video_id, capture_interval = 5):
    # Capture images from the video
    try:
        # Set the start time
        start_time = time.time()
        print(f'start time {start_time}')

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
            current_time = time.time()
            print(f'current time {current_time}')
            elapsed_time = (current_time - start_time) / 1000  # Divide by 1000 to get in seconds
            print(f'start time {start_time}')
            print(f'elapsed_time {elapsed_time}')
            if elapsed_time >= capture_interval:
                print('elapsed_time >= capture_interval')
                image_number += 1
                image_file = os.path.join(image_folder, f"image_{video_id}_{image_number}.jpg")
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                Image.fromarray(image).save(image_file)
                start_time = current_time  # Reset start time to current time after an image is captured and saved
            success, image = vidcap.read()

    except KeyboardInterrupt:
        # Kill the youtube-dl process
        youtube_dl_process.terminate()
        download_process.terminate()
                    