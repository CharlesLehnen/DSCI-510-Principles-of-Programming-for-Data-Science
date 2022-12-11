import os
import random
from PIL import Image
import torchvision
from torchvision.io.image import read_image
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image
import torch
import matplotlib.pyplot as plt

# Set path
IMAGE_FOLDER = "data/images/archived"

# Debug image folder path
# if os.path.exists(IMAGE_FOLDER) and os.listdir(IMAGE_FOLDER):
#     print(f"The image folder contains {len(os.listdir(IMAGE_FOLDER))} files.")
# else:
#     print("The image folder does not exist or is empty.")

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

# For debugging
# print(training_set)
# print(validation_set)
# print(test_set)

def detect_and_classify_animals(image_paths):
    # Load the pre-trained model with ***default*** weights
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(
        weights=FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    )
    # Set the model to inference mode
    model.training = False

    saved_labels = []

   # Loop through the images in the specified folder
    for file_path in image_paths:
        image = read_image(file_path)

        # Add a third dimension to the image tensor
        image = image.unsqueeze(0)

        # Run the model on the image
        outputs = model(image)

        # Extract the bounding boxes and labels
        boxes = outputs[0]["boxes"].detach().numpy()
        labels = outputs[0]["labels"].detach().numpy()

        # Draw the bounding boxes 
        image_with_boxes = draw_bounding_boxes(image, boxes)
        pil_image = to_pil_image(image_with_boxes)

        # Show the image
        plt.imshow(pil_image)
        plt.show()

        # Loop through the detected objects and ask the user to classify species of each one
        for box, label in zip(boxes, labels):
            print(f"Please classify the object in bounding box {box}:")
            user_label = input()

            # Save the label for the object
            saved_labels.append({"box": box, "label": user_label})

        # Save the modified image
        pil_image.save(file_path)

    # Return the list of user-provided labels
    return saved_labels



# Start the manual classification
training_set_labels = detect_and_classify_animals(training_set)
validation_set_labels = detect_and_classify_animals(validation_set)
