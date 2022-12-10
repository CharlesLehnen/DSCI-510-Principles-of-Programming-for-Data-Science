import time
import os
import cv2
from PIL import Image

def capture_images(video_id, capture_interval=15):
    # Capture images from the video
    try:
        start_time = time.time()
        video_output = os.path.join(os.getcwd(), "data", "videos")
        image_folder = os.path.join("data", "images")
        if not os.path.exists(image_folder):
            os.mkdir(image_folder)
        vidcap = cv2.VideoCapture(os.path.join(video_output, f"video_{video_id}.mp4"))
        success, image = vidcap.read()
        count = 0
        while success:
            if count % capture_interval == 0:
                image_file = os.path.join(image_folder, f"image_{video_id}_{count}.jpg")
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                Image.fromarray(image).save(image_file)
            success, image = vidcap.read()
            count += 1
    except KeyboardInterrupt:
        end_time = time.time()
        runtime = end_time - start_time
        print(f"Total runtime: {runtime} seconds")
