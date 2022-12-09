import json
import os
import requests
import time
import subprocess
import re


# SET PARAMETERS

## Interval between screencaptures (seconds)
interval = 15



# Set URL of YouTube live video
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
first, second = url.split('=')

# Set name of video file
video_file = "video.mp4" + "_" + second


# Download videos

## Use subprocess.run() to run the youtube-dl command in the CL and assign its output to a variable
output = subprocess.run(["youtube-dl", "-f", "mp4", "-o", video_file + "_%(format_id)s_%(segment_time)s.mp4", url], capture_output=True)

## Check to see if the download worked or not
if output.returncode != 0:
    print("youtube-dl command failed with exit code {}".format(output.returncode))
    

# Combine videos

## Use subprocess.run() to run the ffmpeg command in the CL to combine videos
output = subprocess.run(["ffmpeg", "-i", video_file + "_%(format_id)s_%(segment_time)s.mp4", "-c", "copy", video_file], capture_output=True)

# Check to see if the ffmpeg command worked or not
if output.returncode != 0:
    print("ffmpeg command failed with exit code {}".format(output.returncode))
