import time
import os
import cv2
from PIL import Image

def capture_images(video_id, capture_interval=5):
    # Capture images from the video
    try:
        # Set the start time
        start_time = time.time()

        # Set the output and image folders
        video_output = os.path.join(os.getcwd(), "data", "videos")
        image_folder = os.path.join("data", "images")
        if not os.path.exists(image_folder):
            os.mkdir(image_folder)

        # Open the video file
        vidcap = cv2.VideoCapture(os.path.join(video_output, f"video_{video_id}.mp4"))

        # Calculate the capture interval based on the video's frame rate
        frame_rate = vidcap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(capture_interval / frame_rate)

        # Capture images
        success, image = vidcap.read()
        frame_count = 0
        image_number = 1
        last_image_time = time.time()
        while success:
            success, image = vidcap.read()
            if not success:
                break

            # Check if the required time interval has passed since the last image was saved
            current_time = time.time()
            time_passed = current_time - last_image_time
            if time_passed >= capture_interval:
                image_number += 1
                image_file = os.path.join(image_folder, f"image_{video_id}_{image_number}.jpg")
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                Image.fromarray(image).save(image_file)
                last_image_time = current_time  # Save the time when the image was saved

    except KeyboardInterrupt:
        # Kill the youtube-dl process
        youtube_dl_process.terminate()
        download_process.termin
