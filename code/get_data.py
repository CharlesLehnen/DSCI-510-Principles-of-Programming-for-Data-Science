import os
import time
import subprocess
import cv2
import ffmpeg
import youtube_dl
import io
from pytube import YouTube
from urllib.parse import urlparse

# SET PARAMETERS

INTERVAL = 15
MAX_RUNTIME = 3
VIDEO_LENGTH = 5


# Set URL of YouTube live video and names
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
parsed_url = urlparse(url)
video_id = parsed_url.query.split("&")[0].split("=")[1]



# Set up folder structure

## Set the video and image folders
video_folder = os.path.join("data", "videos")
if not os.path.exists(video_folder):
    os.mkdir(video_folder)

image_folder = os.path.join("data", "images")
if not os.path.exists(image_folder):
    os.mkdir(image_folder)
   
    
# Download video

output_file = os.path.join(video_folder, f"video_{video_id}_trimmed.mp4")

# Set the maximum runtime in seconds
max_runtime = 10

try:
    # Run the download and processing commands with a maximum runtime
    subprocess.run("youtube-dl -o {} --format mp4 {} | ffmpeg -i - -t {} {}".format(output_file, url, str(max_runtime), output_file), shell=True, timeout=max_runtime)
except subprocess.CalledProcessError:
    # Print a message indicating that the commands timed out
    print("Download and processing timed out after {} seconds".format(max_runtime))



'''

#this worked some of the time, otherwise export mp4.part
video_output = os.path.join(os.getcwd(), "data", "videos")

command = [
    "youtube-dl",
    "--output", f"{video_output}/video_%(id)s.%(ext)s",
    url
]

# Download the video using youtube-dl
subprocess.run(command, timeout = VIDEO_LENGTH)


print("done with stream step")


#might need to do this, but will download to my local machine which is clunkier
#output = youtube_dl.YoutubeDL({"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"}).extract_info(url, download=True)

## Debug
if 'returncode' in stream and stream['returncode'] != 0:
    print("youtube-dl command failed with exit code {}".format(stream['returncode']))
    


# Set up video capture using ffmpeg
ffmpeg_command = "ffmpeg -i {} -acodec copy -vcodec copy -f mpegts pipe:".format(stream["url"])
ffmpeg_process = subprocess.Popen(ffmpeg_command.split(), stdout=subprocess.PIPE)
print("done with ffmpeg step")

# Trying to use this buffer process to fix error
buffer = io.BytesIO()
buffer.write(ffmpeg_process.stdout.read())
buffer.seek(0)
cap = cv2.VideoCapture(buffer)
print("done with buffer step")

# Get correct video stream
video_stream = cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
print("done with video_stream step")


# Capture frames from the stream

start_time = time.time()
print(start_time)

while cap.isOpened():
    # Capture a frame
    ret, frame = cap.read(video_stream)
    if ret:
        # Save the frame
        cv2.imwrite(os.path.join(video_folder, "clip_{:05d}.png".format(counter)), frame)
        
        ## Debug
        if len(os.listdir(video_folder)) > 0:
            print("Video frames saved to: {}".format(video_folder))
        else:
            print("Error saving video frames to: {}".format(video_folder))

        # Extract an image
        cv2.imwrite(os.path.join(image_folder, "image_{:05d}.png".format(counter)), image)
        
        ## Debug
        if len(os.listdir(image_folder)) > 0:
            print("Images saved to: {}".format(image_folder))
        else:
            print("Error saving images to: {}".format(image_folder))

        # Sleep
        time.sleep(INTERVAL)
        counter += 1
       
    # Stop capture
    elapsed_time = time.time() - start_time
    if elapsed_time <= MAX_RUNTIME:
        cap.release()
        
        
'''
     
