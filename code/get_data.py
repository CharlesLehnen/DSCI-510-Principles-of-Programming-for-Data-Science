import os
import time
import subprocess
import cv2
import ffmpeg
import youtube_dl

# SET PARAMETERS

## Interval between screencaptures (seconds)
interval = 15



# Set URL of YouTube live video and names
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
first, second = url.split('=')


# Set the video folder
video_folder = "videos" + "_" + second
if not os.path.exists(video_folder):
    #subprocess.run("mkdir " + video_folder)
    #subprocess.run("mkdir", video_folder)
    #subprocess.run(["C:\\Windows\\System32\\cmd.exe", "/c", "mkdir", video_folder])
    os.mkdir(video_folder)

# Set the image folder
image_folder = "images" + "_" + second
if not os.path.exists(image_folder):
    #subprocess.run("mkdir " + video_folder)
    #subprocess.run("mkdir", image_folder)
    #subprocess.run(["C:\\Windows\\System32\\cmd.exe", "/c", "mkdir", image_folder])
    os.mkdir(image_folder)


# Download video

stream = youtube_dl.YoutubeDL({"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"}).extract_info(
    url, download=False
)

## Check to see if the download worked or not
if stream.returncode != 0:
    print("youtube-dl command failed with exit code {}".format(output.returncode))
    


# Set up video capture using ffmpeg and cv2
cap = cv2.VideoCapture(ffmpeg.input(stream["url"]))

# Capture video clips and extract images
counter = 0
while cap.isOpened():
    # Capture a frame
    ret, frame = cap.read()
    if ret:
        # Save the frame
        cv2.imwrite(os.path.join(video_folder, "clip_{:05d}.png".format(counter)), frame)

        # Extract an image
        cv2.imwrite(os.path.join(image_folder, "image_{:05d}.png".format(counter)), image)

        # Sleep
        time.sleep(interval)
        counter += 1
    else:
        break

# Stop video capture
cap.release()