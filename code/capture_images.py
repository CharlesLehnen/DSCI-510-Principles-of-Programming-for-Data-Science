import time
import os
import cv2
from PIL import Image
from urllib.parse import urlparse
import multiprocessing
from functools import partial

def capture_images(url, capture_interval = 600):
    
    # Extract video_id from url
    parsed_url = urlparse(url)
    video_id = parsed_url.query.split("&")[0].split("=")[1]
    
    # Capture images from the video
    try:
        # Set the output and image folders
        video_output = os.path.join(os.getcwd(), "data", "videos")
        image_folder = os.path.join("data", "images")
        if not os.path.exists(image_folder):
            os.mkdir(image_folder)
        
        # Code to start at image name that was left off at
        
        image_files = os.listdir(image_folder)
        ## Filter, extract, and sort
        image_files = [f for f in image_files if f.startswith(f"image_{video_id}_") and f.endswith(".jpg")]
        image_numbers = [int(f.split("_")[-1].split(".")[0]) for f in image_files]
        image_numbers.sort()

        ## Extract number from last image
        last_image_number = image_numbers[-1]
        
        ## Set new image number
        image_number = last_image_number
        
        # Open the video file
        vidcap = cv2.VideoCapture(os.path.join(video_output, f"video_{video_id}.mp4"))

        # Capture images
        success, image = vidcap.read()

        while success:
            image_number += 1
            timestamp = time.time()
            time_str = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))
            image_file = os.path.join(image_folder, f"image_{video_id}_{image_number}_{time_str}.jpg")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            Image.fromarray(image).save(image_file)
            print(f"Image for video {video_id} captured")
            time.sleep(capture_interval)  # Sleep for the specified capture interval
            success, image = vidcap.read()
                    

    except KeyboardInterrupt:
        print("Keyboard Interrupt")


if __name__ == "__main__":
    # Set the URLs of the YouTube live videos and run
    urls = ["https://www.youtube.com/watch?v=ydYDqZQpim8", "https://www.youtube.com/watch?v=gUZjDCZEMDA"]
    # Original link does not work right now: "https://www.youtube.com/watch?v=UeB6UcZpUzk"
    
    # Set interval between image captures
    capture_interval = 120
    
    with multiprocessing.Pool() as pool:
        pool.map(partial(capture_images, capture_interval = capture_interval), urls)