import os
import random
from PIL import Image

# Path to the folder containing the image files
IMAGE_FOLDER = "data/images"

# Create lists to hold the paths to the training, validation, and test image sets
training_set = []
validation_set = []
test_set = []