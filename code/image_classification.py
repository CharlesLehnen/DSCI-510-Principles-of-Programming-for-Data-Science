import os
from torchvision.io.image import read_image
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image, crop
import torch
import random
from PIL import Image
from torch.utils.data import Dataset
from torchvision.transforms import ToTensor, Compose
from matplotlib.pyplot import imshow
from torchvision.transforms.functional import to_pil_image

# Folder containing images to process
image_dir = "data/images"

# Folder for cropped images
cropped_dir = os.path.join(image_dir, "cropped")

# Create a dictionary to map image filenames to their classification labels
# This will be filled in with user-provided classification values
image_labels = {}

# Create the cropped directory if it doesn't exist
if not os.path.exists(cropped_dir):
    os.makedirs(cropped_dir)

# Define a custom dataset class that wraps the cropped images and their labels
class AnimalDataset(Dataset):
    def __init__(self, image_dir, transform):
        # Store the list of image filenames and labels
        self.image_filenames = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir)]
        # Skip processing filenames that are directories
        self.image_filenames = [filename for filename in self.image_filenames if not os.path.isdir(filename)]
        self.image_labels = [image_labels.get(os.path.basename(filename), 'unknown') for filename in self.image_filenames]
        
        # Store the transforms object
        self.transform = transform

    def __len__(self):
        # Return the length of the dataset
        return len(self.image_filenames)

    def __getitem__(self, index):
        # Read the image and its corresponding label
        image = read_image(self.image_filenames[index])
        label = self.image_labels[index]

        # Apply the transform to the image
        if self.transform:
            image = self.transform(image)

        # Return the image and its label as a tuple
        return image, label
    
    def add_image(self, filename, label):
        # Add the image and its label to the dataset
        self.image_filenames.append(filename)
        self.image_labels.append(label)

def split_dataset(image_dir):
    # Get filenames and shuffle
    filenames = [filename for filename in os.listdir(image_dir)]
    # Remove folders
    filenames = [filename for filename in filenames if not os.path.isdir(os.path.join(image_dir, filename))]
    random.shuffle(filenames)

    # Randomly assign approximately 70% filenames to training, 20% to validation, and %10 to test
    train_filenames = filenames[:int(len(filenames) * 0.7)]
    valid_filenames = filenames[int(len(filenames) * 0.7):int(len(filenames) * 0.9)]
    test_filenames = filenames[int(len(filenames) * 0.9):]

    return train_filenames, valid_filenames, test_filenames


def classify_and_crop(image_dir, cropped_dir):    
    # Initialize the AnimalDataset object
    # Pass the `transform` argument to the constructor
    dataset = AnimalDataset(image_dir, transform)
    
    # Step 1: Initialize model with the best available weights
    ## Change parameter here to adjust!!
    weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = fasterrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=0.5)
    model.eval()

    # Step 2: Initialize the inference transforms
    preprocess = weights.transforms()

    # Separate into sets
    
    ## Get filenames and shuffle
    filenames = [filename for filename in os.listdir(image_dir)]
    # Remove folders
    filenames = [filename for filename in filenames if not os.path.isdir(os.path.join(image_dir, filename))]
    random.shuffle(filenames)

    ## Randomly assign approximately 70% filenames to training, 20% to validation, and %10 to test
    train_filenames = filenames[:int(len(filenames) * 0.7)]
    valid_filenames = filenames[int(len(filenames) * 0.7):int(len(filenames) * 0.9)]
    test_filenames = filenames[int(len(filenames) * 0.9):]
    
    filename = None

    # Process training and validation files in the image directory
    for filename in train_filenames + valid_filenames:
        pass
        # Skip directories
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

        # Save the bounded image
        im.save(os.path.join(cropped_dir, filename))



        # Crop each image to the bounding box for each animal and save it to the cropped_dir directory
        for i, box in enumerate(prediction["boxes"]):
            # Convert float values to integers
            box = torch.round(box)
            x1, y1, x2, y2 = box
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            # Compute the coordinates of the crop region based on the bounding box coordinates
            top = y1
            left = x1
            height = y2 - y1
            width = x2 - x1

            # Crop the image
            cropped_im = crop(im, top, left, height, width)

            # Save the image
            path = os.path.join(cropped_dir, f"{filename}_{i}.jpg")
            cropped_im.save(path)

            # Show the image
            img = Image.open(path)
            img.show()
            
            # Ask the user to classify the detected object
            label = input(f"Enter a classification label for the object in box {i+1}: ")
            if label not in image_labels:
                # If the label does not exist in the dictionary, add it
                image_labels[label] = []
            # Append the filename to the list of filenames for this label
            image_labels[label].append(filename)

            # Add the image and label to the dataset
            dataset.add_image(os.path.join(cropped_dir, f"{filename}_{i+1}.png"), label)
            
    return train_filenames, valid_filenames, test_filenames
            
            
# Ask the user if they want to run the function
should_run = input("Do you want to run the classify_and_crop function? (y/n)")

# Check the user's response and run the function if they want to
if should_run.lower() == "y":
    transform = Compose([
        ToTensor()
    ])
    train_filenames, valid_filenames, test_filenames = classify_and_crop(image_dir, cropped_dir)
else:
    print("The classify_and_crop function will not be run at this time.")

print(f'Image dictionary: {image_labels}')
print(f'Training filenames: {train_filenames}', f'Validation filenames: {valid_filenames}', f'Test filenames: {test_filenames}')