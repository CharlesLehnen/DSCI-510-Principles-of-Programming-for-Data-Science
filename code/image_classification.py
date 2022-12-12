import os
from torchvision.io.image import read_image
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image, crop
import torch
import random

# Directory containing images to process
image_dir = "data/images"

# Directory to save the cropped images
cropped_dir = os.path.join(image_dir, "cropped")

# Create the cropped directory if it doesn't exist
if not os.path.exists(cropped_dir):
    os.makedirs(cropped_dir)

def classify_and_crop(image_dir, cropped_dir):    
    # Step 1: Initialize model with the best available weights
    ## Change parameter here to adjust!!
    weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = fasterrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=0.5)
    model.eval()

    # Step 2: Initialize the inference transforms
    preprocess = weights.transforms()

    # Process all images in the image directory
    for filename in os.listdir(image_dir):
        # Skip subdirectories
        if os.path.isdir(os.path.join(image_dir, filename)):
            continue

        # Read the image
        img = read_image(os.path.join(image_dir, filename))

        # Apply inference preprocessing transforms
        batch = [preprocess(img)]

        # Use the model and visualize the prediction
        prediction = model(batch)[0]
        labels = [weights.meta["categories"][i] for i in prediction["labels"]]
        box = draw_bounding_boxes(img, boxes=prediction["boxes"],
                                  labels=labels,
                                  colors="red",
                                  width=4, font_size=30)
        im = to_pil_image(box.detach())

        # Save the cropped image
        im.save(os.path.join(cropped_dir, filename))



        # Crop each image to the bounding box for each animal
        # and save it to the cropped_dir directory
        for i, box in enumerate(prediction["boxes"]):
            # Convert float values to integers
            box = torch.round(box)
            x1, y1, x2, y2 = box
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            # Compute the coordinates of the crop region
            # based on the bounding box coordinates
            top = y1
            left = x1
            height = y2 - y1
            width = x2 - x1

            # Crop the image
            cropped_im = crop(im, top, left, height, width)

            # Save the cropped image
            cropped_im.save(os.path.join(cropped_dir, f"{filename}_{i}.jpg"))
        


        


