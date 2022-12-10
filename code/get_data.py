import time
import subprocess
import os
from urllib.parse import urlparse
from PIL import Image

def download_video(url, capture_interval=1):
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
        "--output", f"{video_output}/video_%(id)s.%(ext)s",
        "--no-part",
        url
    ]

    # Start the youtube_dl_process
    youtube_dl_process = subprocess.Popen(command)

    # Capture images from the video
    try:
        start_time = time.time()
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

if __name__ == "__main__":
    # Set the URL of the YouTube live video and run
    url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
    download_video(url)
