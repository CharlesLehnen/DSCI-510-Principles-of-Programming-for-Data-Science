import json
import os
import requests
import time
import subprocess
import re


# SET PARAMETERS

## Max number of screencaptures
max_iterations = 3
## Interval between screencaptures (seconds)
interval = 2



# Set URL of YouTube live video
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
first, second = url.split('=')

# Set the time interval (in seconds) for image extraction
interval = 2

# Set the name of the folder for images
screencaptures_folder = "images" + "_" + second
if not os.path.exists(screencaptures_folder):
    subprocess.run(["C:\\Windows\\System32\\cmd.exe", "/c", "mkdir", screencaptures_folder])

# Set-up a folder for metadata
metadata_folder = "metadata" + "_" + second
if not os.path.exists(metadata_folder):
    subprocess.run(["C:\\Windows\\System32\\cmd.exe", "/c", "mkdir", metadata_folder])

    
# Collect metadata
     
counter = 0

while counter < max_iterations :
    # Use subprocess.run() to run the youtube-dl command in the CL and assign its output to a variable
    output = subprocess.run(["youtube-dl", "--write-info-json", "--output", os.path.join(metadata_folder, "%(id)s.info.json"), url], capture_output=True)


    # Check to see if worked or not
    if output.returncode != 0:
        print("youtube-dl command failed with exit code {}".format(output.returncode))
        break

    # Sleep between extractions
    time.sleep(interval)
    counter += 1
    print("Successfully downloaded metadata for {url} x {counter}".format(url = url, counter = counter))


# Iterate over metadata

for filename in os.listdir(metadata_folder):
    
    # Open and read the metadata
    with open(os.path.join(metadata_folder, filename), encoding="utf-8") as f:
        metadata_str = f.read()

    # Use ftfy to clean up the metadata string so it stops throwing errors
    metadata_str = re.sub(r'[^\x00-\x7f]', '?', metadata_str)
    metadata = json.loads(metadata_str)

    print("Downloading image from {}".format(metadata["thumbnail"]["url"]))
        
    # Download the thumbnail image from the URL listed in the metadata
    response = requests.get(metadata["thumbnail"]["url"])
    
    # Save the thumbnail to screencaptures folder
    with open(os.path.join(screencaptures_folder, metadata["id"] + "." + metadata["thumbnail"]["format"]), "wb") as f:
        f.write(response.content)
    print("Image downloaded")
