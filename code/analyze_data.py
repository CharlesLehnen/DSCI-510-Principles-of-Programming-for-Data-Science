import os
import pandas as pd
import seaborn as sns

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

# Print results
# print(files)
# print(file_dict)

# Create pandas dataframe from the dictionary
df = pd.DataFrame(columns=['video_id', 'timestamp', 'count'])
for key, value in file_dict.items():
    count = len(value)
    new_df = pd.DataFrame({'video_id': [video_id], 'timestamp': [timestamp], 'count': [count]})
    df = pd.concat([df, new_df], ignore_index=True)


    
# Set the video_id column as the index of the dataframe
df = df.set_index('video_id')

# Convert the timestamp column to a datetime object
df['timestamp'] = pd.to_datetime(df['timestamp'].values, format='%Y-%m-%d_%H-%M-%S')

# Convert the 'count' column to a numerical data type
df['count'] = pd.to_numeric(df['count'])

print(df.dtypes)


# # Group the data by timestamp and aggregate the counts
# df = df.groupby('timestamp')['count'].sum()

# # Set the style of the plot
# sns.set_style('darkgrid')

# # Create the lineplot
# ax = sns.lineplot(x=df['timestamp'].values, y=df['count'].values)

# # Set the labels for the x and y axes
# ax.set(xlabel='Timestamp', ylabel='Count')

# # Show the plot
# plt.show()