import json
import os
import requests
import time
import subprocess

# Set URL of YouTube live video
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
first, second = url.split('=')

# Set the time interval (in seconds) for image extraction
interval = 10

# Set the name of the folder for images
screencaptures_folder = "images" + "_" + second
if not os.path.exists(screencaptures_folder):
    os.mkdir(screencaptures_folder)

# Set-up a folder for metadata
metadata_folder = "metadata" + "_" + second
if not os.path.exists(metadata_folder):
    os.mkdir(metadata_folder)

# Set the path to the youtube-dl executable
youtube_dl_path = r"C:\Path\To\youtube-dl.exe"

while True:
    # Use subprocess.check_output to run the youtube-dl command and capture its output
    output = subprocess.check_output([youtube_dl_path, "--write-info-json", "--output", "%(id)s.info.json", url])

    # Check the exit code of the youtube-dl command to determine if it was successful
    if output.returncode != 0:
        print("youtube-dl command failed with exit code {}".format(output.returncode))
        break

    # Sleep between extractions
    time.sleep(interval)


# Iterate over metadata files in metadata folder

for filename in os.listdir(metadata_folder):
    
    # Open the metadata from the file
    with open(os.path.join(metadata_folder, filename)) as f:
        metadata = json.load(f)
        
    # Download the thumbnail image from the URL indicated by metadata
    response = requests.get(metadata["thumbnail"]["url"])
    
    # Save thumbnail to screencaptures folder
    with open(os.path.join(screencaptures_folder, metadata["id"] + "." + metadata["thumbnail"]["format"]), "wb") as f:
        f.write(response.content)
