import time
import os
import cv2
from PIL import Image
from urllib.parse import urlparse
import multiprocessing
from functools import partial

def capture_images(url, capture_interval = 300):
    # Delay for capture_interval seconds before starting the capture process
    time.sleep(capture_interval)
    
    # Extract video_id from url
    parsed_url = urlparse(url)
    video_id = parsed_url.query.split("&")[0].split("=")[1]
    
    # Capture images from the video
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Extract video_id from url
        parsed_url = urlparse(url)
        video_id = parsed_url.query.split("&")[0].split("=")[1]

        # Set the output and image folders
        video_output = os.path.join(script_dir, "data", "videos")

        image_folder = os.path.join(script_dir, "data", "images")
        if not os.path.exists(image_folder):
            os.mkdir(image_folder)
        
        # Code to start at image name that was left off at
        image_files = os.listdir(image_folder)
        ## Filter, extract, and sort
        image_files = [f for f in image_files if f.startswith(f"image_{video_id}_") and f.endswith(".jpg")]
        image_numbers = [int(f.split("_")[-1].split(".")[0]) for f in image_files]
        image_numbers.sort()

        ## Extract number from last image or set to 0 if no images found
        last_image_number = image_numbers[-1] if image_numbers else 0
                
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
            image_file = os.path.join(image_folder, f"image_{video_id}_{time_str}_{image_number}.jpg")
            #image_file = os.path.join(image_folder, f"image_{video_id}_{image_number}.jpg")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            Image.fromarray(image).save(image_file)
            print(f"Image for video {video_id} captured")
            time.sleep(capture_interval)  # Sleep for the specified capture interval
            success, image = vidcap.read()
                    

    except KeyboardInterrupt:
        print("Keyboard Interrupt")


def main(urls=None, capture_interval=None):
    if not urls:
        # Prompt the user for URLs or use default values
        user_urls = input("Enter the YouTube video URLs separated by commas or press Enter to use default: ").strip()
        if user_urls:
            urls = [url.strip() for url in user_urls.split(",")]
        else:
            # Default URLs
            urls = ["https://www.youtube.com/watch?v=ydYDqZQpim8"]

    if not capture_interval:
        # Prompt the user for capture_interval or use default value
        try:
            user_interval = int(input(f"Enter the capture interval in seconds or press Enter to use default ({300} seconds): ").strip())
            capture_interval = user_interval
        except ValueError:
            capture_interval = 300

    with multiprocessing.Pool() as pool:
        pool.map(partial(capture_images, capture_interval=capture_interval), urls)

if __name__ == "__main__":
    main()