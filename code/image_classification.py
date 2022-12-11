import os
import torch
import torchvision
import cv2
from PIL import Image
from torchvision import transforms

FILE_PATH = "data/images/archived"

# Load VggNet model
model = torchvision.models.vgg16(pretrained=True)

# Define preprocessing transformation
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Loop through images
for filename in os.listdir(FILE_PATH):
  # Load the image and convert it to a PIL.Image
  image = cv2.imread(os.path.join(FILE_PATH, filename))
  image = Image.fromarray(image)

  # Apply the transformation
  image = transform(image)

  # Add an extra dimension to the image to make it compatible
  image = image.unsqueeze(0)

  # Use the model to make predictions
  with torch.no_grad():
    output = model(image)

  # Get the class with the highest probability
  _, predicted = torch.max(output, 1)

  # Print predicted class
  print(predicted)
