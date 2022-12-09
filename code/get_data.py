import os
import time

# Set URL of YouTube live video
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"

# Set the time interval (in seconds) for image extraction
interval = 30

# Set the name of the folder for images
folder_name = "images" + "_" + url

# Create new folder if does not exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

while True:
    # Use ffmpeg to extract an image from the video at the specified time interval
    os.system(f"ffmpeg -i {url} -vf fps=1/{interval} -vframes 1 {folder_name}/image.jpg")

    # Sleep for the specified interval before extracting another image
    time.sleep(interval)
