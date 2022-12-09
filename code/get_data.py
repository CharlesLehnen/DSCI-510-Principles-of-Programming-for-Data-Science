import os
import time

# Set URL of YouTube live video
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
first, second = url.split('=')

# Use youtube-dl to extract the streaming URL of the video
stream_url = os.system(f"youtube-dl -g -f worst {url} > stream-url")

# Set the time interval (in seconds) for image extraction
interval = 10

# Set the name of the folder for images
folder_name = "images" + "_" + second

# Create new folder if does not exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

while True:
    # Generate timestamp for image
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())

    # Use ffmpeg to try to extract images at set intervals
    os.system(f"ffmpeg -i $(cat stream-url) -f image2 -frames:v 1 {folder_name}/img22_{timestamp}.jpeg")

    # Sleep between extractions
    time.sleep(interval)
