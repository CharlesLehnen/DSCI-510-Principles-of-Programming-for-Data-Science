import os
import random
import torchvision
from PIL import Image
import torchvision.transforms as transforms

# Set path
IMAGE_FOLDER = "data/images/archived"

# Create empthy lists for training, validation, and test image sets
training_set = []
validation_set = []
test_set = []

# Randomly assign approximately 70% images to training, 20% to validation, and %10 to test
for file_name in os.listdir(IMAGE_FOLDER):
    file_path = os.path.join(IMAGE_FOLDER, file_name)
    
    # Random binanry
    random_number = random.random()
    
    # Add the file to the appropriate set (training, validation, or test)
    if random_number < 0.7:
        training_set.append(file_path)
    elif random_number < 0.9:
        validation_set.append(file_path)
    else:
        test_set.append(file_path)

# # Create empty lists for the updated image sets
# updated_training_set = []
# updated_validation_set = []
# updated_test_set = []

# # Update file paths using os.path.join so that I don't have problems
# for image in training_set:
#     updated_image = os.path.join(IMAGE_FOLDER, image)
#     updated_training_set.append(updated_image)
    
# for image in validation_set:
#     updated_image = os.path.join(IMAGE_FOLDER, image)
#     updated_validation_set.append(updated_image)
    
# for image in test_set:
#     updated_image = os.path.join(IMAGE_FOLDER, image)
#     updated_test_set.append(updated_image)
    
# Load the model
model = torchvision.models.detection.fasterrcnn_resnet50_fpn()

# Set the model to evaluation mode
model.eval()

# Loop over the images in your dataset
for image_path in training_set + validation_set + test_set:
    # Load the image and convert it to a tensor
    image = Image.open(image_path)
    transform = transforms.ToTensor()
    image_tensor = transform(image)
    
    # Use the model to detect objects in the image and draw bounding boxes around them
    outputs = model(image_tensor)
    for output in outputs:
        bbox = output['boxes']  # Coordinates of the bounding box
        # Use the bounding box coordinates to crop the image
        cropped_image = image_tensor[:, bbox[0]:bbox[2], bbox[1]:bbox[3]]
        # Save the cropped image to a folder
        torchvision.utils.save_image(cropped_image, os.path.join(save_folder, f'{i}.jpg'))
        i += 1