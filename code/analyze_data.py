import seaborn as sns
from seaborn import FacetGrid
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create empty dict
file_dict = {}

# Get list of files in directory
files = os.listdir('data/images/cropped')

# Loop through the files
for file in files:
    # Split the filenames
    parts = file.split('_')
    if parts[0] == 'image':
        video_id = parts[1]
        timestamp = parts[2] + "_" + parts[3]
        # Create a key for the dictionary using the video_id and timestamp
        key = f"{video_id}_{timestamp}"
        # If the key doesn't exist in the dictionary, create a new list for it
        if key not in file_dict:
            file_dict[key] = []
        # Append the file path to the list of file paths for this key
        file_dict[key].append(os.path.join('data/images/cropped', file))
        
# Convert to Pandas dataframe
rows = []
for key, value in file_dict.items():
    video_id = key.split("_")[0]
    timestamp = key.split("_")[1] + "_" + key.split("_")[2]
    count = len(value)
    rows.append((video_id, timestamp, count))


df = pd.DataFrame(rows, columns=["video_id", "timestamp", "count"])
df['timestamp']=pd.to_datetime(df['timestamp'],format='%Y-%m-%d_%H-%M-%S')


# Set the timestamp column as the index of the dataframe
df.set_index("timestamp", inplace=True)

# Use seaborn to plot the timeseries
sns.lineplot(data=df)
plt.xticks(rotation=45)
