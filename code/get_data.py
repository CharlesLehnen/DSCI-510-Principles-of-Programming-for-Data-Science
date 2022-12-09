import os
import time
import subprocess

# Set URL of YouTube live video
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
first, second = url.split('=')

# Use youtube-dl to extract the streaming URL of the video
output = subprocess.run(["youtube-dl", "-g", "-f", "worst", url], capture_output=True)

# Save the streaming URL to a file
with open("stream-url", "w") as f:
    f.write(output.stdout.decode("utf-8"))

# Set the time interval (in seconds) for image extraction
interval = 10

# Set the name of the folder for images
folder_name = "images" + "_" + second

# Create new folder if does not exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

while True:
    # Generate timestamp for image naming
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())

    # Use ffmpeg to try to extract images at set intervals
    os.system(f"ffmpeg -i {stream_url_contents} -vcodec copy {folder_name}/img_{timestamp}.jpeg")

    # Sleep between extractions
    time.sleep(interval)
