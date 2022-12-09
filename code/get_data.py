import os
import time

# Set URL of YouTube live video
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
first, second = url.split('=')

# Set the time interval (in seconds) for image extraction
interval = 10

# Set the name of the folder for images
folder_name = "images" + "_" + second

# Create new folder if does not exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

while True:
    # Use ffmpeg to try to extract images at set intervals
    os.system(f"ffmpeg -i {url} -vf fps=1/{interval} -vframes 1 {folder_name}/image%d.jpg")

    # Sleep between extractions
    time.sleep(interval)
