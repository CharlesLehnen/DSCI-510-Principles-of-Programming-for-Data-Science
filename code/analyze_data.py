import os
from collections import defaultdict

# Create a dictionary that uses a list
filename_dict = defaultdict(list)

# Set the file path
dir_path = 'data/images/cropped'

# Iterate through filenames in the folder
for filename in os.listdir(dir_path):
  # Split the filename into parts
  parts = filename.split('_')
  
  # Check if the filename has the expected format
  if len(parts) == 4 and parts[0] == 'image' and parts[3].endswith('.jpg'):
    # Create a unique key by concatenating the video_id and time_str parts
    key = parts[1] + '_' + parts[2]
    # Add the full filename to the list of values for the key
    filename_dict[key].append(os.path.join(dir_path, filename))

# Print result
print(dict(filename_dict))
