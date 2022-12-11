import os
import torch
import torchvision
import cv2
from PIL import Image
from torchvision import transforms
from torchvision.models.vgg import VGG16_Weights
import subprocess

# Install ILSVRC2012_devkit_t12 if not already installed

## Set the root directory and file name
root_dir = "data/imagenet"
file_name = "ILSVRC2012_devkit_t12.tar.gz"
file_url = "http://www.image-net.org/challenges/LSVRC/2012/nnoupb/" + file_name

## Check if the file is already present
if not os.path.exists(os.path.join(root_dir, file_name)):
    # Download the file
    subprocess.run(["wget", file_url, "-P", root_dir])


FILE_PATH = "data/images/archived"

# Load VggNet model
model = torchvision.models.vgg16(weights=VGG16_Weights.IMAGENET1K_V1)
imagenet_dataset = torchvision.datasets.ImageNet(root="data/imagenet", split="val")

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

    # Use the model to make predictions
    with torch.no_grad():
        output = model(transform(Image.fromarray(image)).unsqueeze(0))

    # Get the class with the highest probability
    _, predicted = torch.max(output, 1)
    
    # Print the predicted classes
    class_names = imagenet_dataset.label_mapping
    predicted_class_name = imagenet_dataset.label_mapping[predicted]
    print("Predicted class index:", predicted)
    print("Predicted class names:", predicted_class_name)

    # Use the VGG16 model to detect animals
    if predicted == "animals":
        # Use OpenCV to detect animals in the image
        animal_cascade = cv2.CascadeClassifier("data/cascades/animals.xml")
        animals = animal_cascade.detectMultiScale(image, scaleFactor=1.05, minNeighbors=5)
        
        # Print the number of detected animals
        print("Number of detected animals:", len(animals))

        # Loop through detected animals
        for (x, y, w, h) in animals:
            # Create a bounding box around the animal
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Crop the image to the bounding box and save it
            cropped_image = image[y:y+h, x:x+w]
            cv2.imwrite(f"cropped/{filename}", cropped_image)
            if not os.path.exists(cropped):
                os.mkdir(cropped)
            cv2.imwrite(f"cropped/{filename}", cropped_image)

