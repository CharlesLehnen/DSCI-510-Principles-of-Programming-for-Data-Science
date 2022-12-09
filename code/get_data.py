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



# Set up folder structure

## Set the video and image folders
video_folder = os.path.join("data", "videos" + "_" + second)
if not os.path.exists(video_folder):
    os.mkdir(video_folder)

image_folder = os.path.join("data", "images" + "_" + second)
if not os.path.exists(image_folder):
    os.mkdir(image_folder)
    
## Double-check folders
if os.path.exists(video_folder):
    print("Video folder created: {}".format(video_folder))
else:
    print("Error creating video folder: {}".format(video_folder))

if os.path.exists(image_folder):
    print("Image folder created: {}".format(image_folder))
else:
    print("Error creating image folder: {}".format(image_folder))
    
if len(os.listdir(video_folder)) > 0:
    print("Video frames saved to: {}".format(video_folder))
else:
    print("Error saving video frames to: {}".format(video_folder))

if len(os.listdir(image_folder)) > 0:
    print("Images saved to: {}".format(image_folder))
else:
    print("Error saving images to: {}".format(image_folder))

'''

# Download video

stream = youtube_dl.YoutubeDL({"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"}).extract_info(url, download=False)

#might need to do this, but will download to my local machine which is clunkier
#output = youtube_dl.YoutubeDL({"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"}).extract_info(url, download=True)

## Check to see if the download worked or not
if 'returncode' in stream and stream['returncode'] != 0:
    print("youtube-dl command failed with exit code {}".format(stream['returncode']))
    


# Set up video capture using ffmpeg and cv2
ffmpeg_command = "ffmpeg -i {} -acodec copy -vcodec copy -f mpegts pipe:".format(stream["url"])
ffmpeg_process = subprocess.Popen(ffmpeg_command.split(), stdout=subprocess.PIPE)
cap = cv2.VideoCapture(ffmpeg_process.stdout)

# Debug
print("Video capture object:")
print(cap)
ret, frame = cap.read()
print("Frame data:")
print(frame)

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

'''