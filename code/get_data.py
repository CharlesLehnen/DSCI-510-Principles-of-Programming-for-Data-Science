import os
import time
import subprocess
import cv2
import ffmpeg
import youtube_dl
import io

# SET PARAMETERS

INTERVAL = 15
MAX_RUNTIME = 3



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
    
## Debug
if os.path.exists(video_folder):
    print("Video folder created: {}".format(video_folder))
else:
    print("Error creating video folder: {}".format(video_folder))

if os.path.exists(image_folder):
    print("Image folder created: {}".format(image_folder))
else:
    print("Error creating image folder: {}".format(image_folder))



#help(youtube_dl.YoutubeDL)
    
# Download video

ydl_opts = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "outtmpl": os.path.join(video_folder, "%(title)s.%(ext)s"),
    "noplaylist": True,
    "timeout": 3,  # Set timeout to 3 seconds
}

ydl = youtube_dl.YoutubeDL(ydl_opts)

try:
    # Download video using youtube-dl
    ydl.download([url])
except:
    # Handle error if download times out
    print("Download timed out after {} seconds".format(ydl_opts["timeout"]))


# ydl_opts = {
#     'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
#     'timeout': 3
# }

# stream = youtube_dl.YoutubeDL(ydl_opts).extract_info(url)

#stream = youtube_dl.YoutubeDL({"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"}).extract_info(url, download=False, timeout=3)



print("done with stream step")

'''

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
     
