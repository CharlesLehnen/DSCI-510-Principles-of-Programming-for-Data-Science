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
    
# This class extends the Dataset from Pytorch with my custom classification value   
class AnimalDataset(Dataset):
    def __init__(self, transform):
        # Initialize empty lists for image filenames and labels
        self.image_filenames = []
        self.image_labels = []

        # Store the transforms object
        self.transform = transform

    def add_image(self, filename, label):
        # Add the image filename and label to the lists
        self.image_filenames.append(filename)
        self.image_labels.append(label)

    def __len__(self):
        # Return the length of the dataset
        return len(self.image_filenames)

    def __getitem__(self, idx):
        # Load the image at the given index
        image = read_image(self.image_filenames[idx])

        # Apply the transforms
        if self.transform:
            image = self.transform(image)

        # Return the image and its label
        return image, self.image_labels[idx]
    
def classify_and_crop(image_dir, cropped_dir):    
    # Initialize the AnimalDataset object
    dataset = AnimalDataset(transform)
    
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

        # # Save
        # im.save(os.path.join(cropped_dir, filename))

        # Crop each image to the bounding box for each animal and save it to the cropped_dir directory
        for i, box in enumerate(prediction["boxes"]):
            # Convert float values to integers
            box = torch.round(box)
            x1, y1, x2, y2 = box
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            # Crop the image
            cropped_img = img[y1:y2, x1:x2]
            
            # Save the cropped image
            im.save(os.path.join(cropped_dir, filename))
            
            # Show the image
            img = Image.open(os.path.join(cropped_dir, filename))
            img.show()
            
            # Ask the user to classify the detected object
            label = input(f"Enter a classification label for the object in box {i+1}: ")
            image_labels[filename] = label

            # Add the image and label to the dataset
            dataset.add_image(os.path.join(cropped_dir, f"{filename}_{i+1}.png"), label)
    
    
#     for filename in os.listdir(image_dir):
#         # Skip subdirectories
#         if os.path.isdir(os.path.join(image_dir, filename)):
#             continue

#         # Read the image
#         img = read_image(os.path.join(image_dir, filename))

#         # Apply inference preprocessing transforms
#         batch = [preprocess(img)]

#         # Use the model and visualize the prediction
#         prediction = model(batch)[0]
#         labels = [weights.meta["categories"][i] for i in prediction["labels"]]
#         box = draw_bounding_boxes(img, boxes=prediction["boxes"],
#                                   labels=labels,
#                                   colors="red",
#                                   width=4, font_size=50)
#         im = to_pil_image(box.detach())
        
        
#         # Crop each image to the bounding box for each animal and save it to the cropped_dir directory
#         for i, box in enumerate(prediction["boxes"]):
#             # Convert float values to integers
#             box = torch.round(box)
#             x1, y1, x2, y2 = box
#             x1 = int(x1)
#             y1 = int(y1)
#             x2 = int(x2)
#             y2 = int(y2)

#             # Crop the image
#             cropped_img = img[y1:y2, x1:x2]

#             # Convert the tensor to a PIL.Image object and show it
#             pil_img = Image.fromarray(cropped_img.mul_(255).permute(1, 2, 0).byte().numpy())
#             pil_img.show()

#             # Ask the user to classify the detected object
#             label = input(f"Enter a classification label for the object in box {i+1}: ")
#             image_labels[filename] = label

#             # Add the image and label to the dataset
#             dataset.add_image(os.path.join(cropped_dir, f"{filename}_{i+1}.png"), label)

#         # Save the cropped image
#         im.save(os.path.join(cropped_dir, filename))

        

#         # Crop each image to the bounding box for each animal and save it to the cropped_dir directory
#         for i, box in enumerate(prediction["boxes"]):
#             # Convert float values to integers
#             box = torch.round(box)
#             x1, y1, x2, y2 = box
#             x1 = int(x1)
#             y1 = int(y1)
#             x2 = int(x2)
#             y2 = int(y2)

#             # Compute the coordinates of the crop region based on the bounding box coordinates
#             top = y1
#             left = x1
#             height = y2 - y1
#             width = x2 - x1

#             # Crop the image
#             cropped_im = crop(im, top, left, height, width)
            
#             # Ask the user to classify the detected object
#             label = input(f"Enter a classification label for the object in box {i+1}: ")
#             image_labels[filename] = label

#             # Add the image and label to the dataset
#             dataset.add_image(os.path.join(cropped_dir, f"{filename}_{i+1}.png"), label)

#             # Save the cropped image
#             cropped_im.save(os.path.join(cropped_dir, f"{filename}_{i}.jpg"))

                                
# Ask the user if they want to run the function
should_run = input("Do you want to run the classify_and_crop function? (y/n)")

# Check the user's response and run the function if they want to
if should_run.lower() == "y":
    transform = Compose([
        ToTensor()
    ])
    classify_and_crop(image_dir, cropped_dir)
else:
    print("The classify_and_crop function will not be run at this time.")
    
    
print(image_labels)
type(list(image_labels.items())[0])

    
# # This class extends the Dataset from Pytorch with my custom classification values
# class AnimalDataset(Dataset):
#     def __init__(self, image_dir, transform):
#         # Store the list of image filenames and labels
#         self.image_filenames = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir)]
#         self.image_labels = [image_labels[os.path.basename(filename)] for filename in self.image_filenames]

#         # Store the transforms object
#         self.transform = transform

#     def __len__(self):
#         # Return the length of the dataset
#         return len(self.image_filenames)

#     def __getitem__(self, index):
#         # Read the image and its corresponding label
#         image = read_image(self.image_filenames[index])
#         label = self.image_labels[index]

#         # Apply the transform to the image
#         if self.transform:
#             image = self.transform(image)

#         # Return the image and its label as a tuple
#         return image, label
    
                

    
'''    

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

            # Save the cropped image
            cropped_im.save(os.path.join(cropped_dir, f"{filename}_{i}.jpg"))
'''
            





# # Step 5: Split the paths of the cropped images into 70% training, 20% validation, and 10% test sets

# cropped_paths = [os.path.join(cropped_dir, filename) for filename in os.listdir(cropped_dir)]

# ## Shuffle the paths
# random.shuffle(cropped_paths)

# ## Split the paths
# train_paths = cropped_paths[:int(len(cropped_paths) * 0.7)]
# valid_paths = cropped_paths[int(len(cropped_paths) * 0.7):int(len(cropped_paths) * 0.9)]
# test_paths = cropped_paths[int(len(cropped_paths) * 0.9):]

## For debugging
## print(f'Training: {train_paths}')
## print(f'Training: {valid_paths}')
## print(f'Training: {test_paths}')


# Manually re-classify images

# (This worked, but trying something else)
# for path in train_paths + valid_paths:
#     # Open the image and display it to the user
#     img = Image.open(path)
#     img.show()

#     # Ask the user to classify the image
#     classification = input("Enter the classification for this image: ")

#     # Store the classification somewhere (e.g. in a database)
#     # ...
    
# Process all images in the image directory
# for filename in os.listdir(image_dir):
#     # Skip subdirectories
#     if os.path.isdir(os.path.join(image_dir, filename)):
#         continue

#     # Read the image and make predictions
#     img = read_image(os.path.join(image_dir, filename))
#     batch = [preprocess(img)]
#     prediction = model(batch)[0]

#     # Draw bounding boxes around each detected object
#     labels = [weights.meta["categories"][i] for i in prediction["labels"]]
#     box = draw_bounding_boxes(img, boxes=prediction["boxes"],
#                               labels=labels,
#                               colors="red",
#                               width=4, font_size=30)
#     im = to_pil_image(box.detach())

#     # Display the image with bounding boxes
#     im.show()

#     # Ask the user to classify each detected object
#     for i, box in enumerate(prediction["boxes"]):
#         label = input(f"Enter a classification label for the object in box {i+1}: ")
#         image_labels[filename] = label

#     # Save the cropped image
#     im.save(os.path.join(cropped_dir, filename))
    
# # Create a custom AnimalDataset object
# transform = Compose([ToTensor(), Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
# dataset = AnimalDataset(image_dir, transform)

# class AnimalDataset(Dataset):
#     def __init__(self, image_dir, transform):
#         # Store the list of image filenames and labels
#         self.image_filenames = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir)]
#         self.image_labels = [image_labels[os.path.basename(filename)] for filename in self.image_filenames]

#         # Store the transforms object
#         self.transform = transform


