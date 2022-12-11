import os
import random
from PIL import Image
import torchvision
from torchvision.io.image import read_image
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image
import torch

# Path to the folder containing the image files
IMAGE_FOLDER = "data/images/archived"
print(IMAGE_FOLDER)


# Create lists to hold the paths to the training, validation, and test image sets
training_set = []
validation_set = []
test_set = []

# Loop through the files in the image folder
for file_name in os.listdir(IMAGE_FOLDER):
    # Compute the path to the file
    file_path = os.path.join(IMAGE_FOLDER, file_name)

    # Add the file to the appropriate set (training, validation, or test)
    # based on its name
    if "training" in file_name:
        training_set.append(file_path)
    elif "validation" in file_name:
        validation_set.append(file_path)
    elif "test" in file_name:
        test_set.append(file_path)

# Print the list of image paths
print(training_set)
print(validation_set)
print(test_set)


# Define the function to process the images and classify the detected objects
def detect_and_classify_animals(image_paths):
    # Load the pre-trained model with the default weights
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(
        weights=FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    )

    # Create a list to hold the user-provided labels for the detected objects
    saved_labels = []

    # Loop through the images in the specified folder
    for file_path in image_paths:
        # Load the image and run it through the model
        image = read_image(file_path)
        print(image)
        outputs = model(image)

        # Extract the bounding boxes and labels for the detected objects
        boxes = outputs[0]["boxes"].detach().numpy()
        labels = outputs[0]["labels"].detach().numpy()

        # Draw the bounding boxes on the image
        image_with_boxes = draw_bounding_boxes(image, boxes)
        pil_image = to_pil_image(image_with_boxes)

        # Loop through the detected objects and ask the user to classify each one
        for box, label in zip(boxes, labels):
            print(f"Please classify the object in bounding box {box}:")
            user_label = input()

            # Save the user-provided label for the object
            # (You could save this in a file or database for later use)
            saved_labels.append({"box": box, "label": user_label})

        # Save the image with the bounding boxes drawn on it
        pil_image.save(file_path)

    # Return the list of user-provided labels for the detected objects
    return saved_labels

# Use the function to process the images in the training set
training_set_labels = detect_and_classify_animals(training_set)

# Use the function to process the images in the validation set
validation_set_labels = detect_and_classify_animals(validation_set)