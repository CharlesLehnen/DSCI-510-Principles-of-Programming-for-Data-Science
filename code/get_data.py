import os
import time
import subprocess
import threading
import io
from urllib.parse import urlparse
import signal

# Create a global variable to store a reference to the youtube_dl_process
youtube_dl_process = None

def download_video(url):
    global youtube_dl_process

    # SET PARAMETERS
    timeout = 7

    # Set URL of YouTube live video and names
    parsed_url = urlparse(url)
    video_id = parsed_url.query.split("&")[0].split("=")[1]

    # Set up folder and file structure
    video_folder = os.path.join("data", "videos")
    if not os.path.exists(video_folder):
        os.mkdir(video_folder)
    output_file = os.path.join(video_folder, f"video_{video_id}_trimmed.mp4")
    image_folder = os.path.join("data", "images")
    if not os.path.exists(image_folder):
        os.mkdir(image_folder)

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

# Set the URL of the YouTube live video
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"

# Start the download_video() function in a separate thread
youtube_dl_thread = threading.Thread(target=download_video, args=(url,))
youtube_dl_thread.start()

# Wait for the specified time
time.sleep(timeout)

# Use the terminate() method of the youtube_dl_process to terminate the youtube_dl_process
youtube_dl_process.terminate()

# Check the return code to see if the youtube_dl_process was terminated
if youtube_dl_process.poll() == -signal.SIGKILL:
    print("The youtube_dl_process was terminated after running for %d seconds" % timeout)



'''

import os
import time
import subprocess
import io
from urllib.parse import urlparse
from subprocess import TimeoutExpired, CalledProcessError
import signal
import threading


import importlib.util

# Check if the threading module exists
threading_spec = importlib.util.find_spec("threading")

# Print the result
if threading_spec:
    print("The threading module was imported correctly")
else:
    print("The threading module was not imported")
    
    

# SET PARAMETERS

timeout = 7

# Set URL of YouTube live video and names
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
parsed_url = urlparse(url)
video_id = parsed_url.query.split("&")[0].split("=")[1]


# Set up folder and file structure

video_folder = os.path.join("data", "videos")
if not os.path.exists(video_folder):
    os.mkdir(video_folder)

image_folder = os.path.join("data", "images")
if not os.path.exists(image_folder):
    os.mkdir(image_folder)
   
  
# Download video

video_output = os.path.join(os.getcwd(), "data", "videos")

command = [
    "youtube-dl",
    "--output", f"{video_output}/video_%(id)s.%(ext)s", # this prevented conflicting naming errors
    "--no-part", # this prevented videos from being exported as .mp4.part
    url
]

# Start the subprocess and run for the specified time
#result = subprocess.run(command, timeout=timeout)

# Start the youtube_dl_process in a separate thread so that I can kill it while it runs in the background
youtube_dl_thread = threading.Thread(target=subprocess.run, args=(command,))
youtube_dl_thread.start()

# Wait for the specified time
time.sleep(timeout)

# Use the terminate() method to terminate the youtube_dl_process
youtube_dl_thread.terminate()

# Check the return code to see if the youtube_dl_process was terminated
if youtube_dl_thread.poll() == -signal.SIGKILL:
    print("The youtube_dl_process was terminated after running for %d seconds" % timeout)
    
'''