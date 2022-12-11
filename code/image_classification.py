import os
import random
from PIL import Image

# Path to the folder containing the image files
IMAGE_FOLDER = "data/images/archived"

# Create lists to hold the paths to the training, validation, and test image sets
training_set = []
validation_set = []
test_set = []

# Randomly split the image files into the different sets, ensuring that each set contains at least one image
for file_name in os.listdir(IMAGE_FOLDER):
    file_path = os.path.join(IMAGE_FOLDER, file_name)
    if len(training_set) < 1:
        training_set.append(file_path)
    elif len(validation_set) < 1:
        validation_set.append(file_path)
    elif len(test_set) < 1:
        test_set.append(file_path)
    else:
        set_to_add_to = random.choice([training_set, validation_set, test_set])
        set_to_add_to.append(file_path)
        
print(training_set)
print(validation_set)
print(test_set)