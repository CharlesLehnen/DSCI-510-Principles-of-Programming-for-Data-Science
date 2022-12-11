import os
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
from torchvision.io.image import read_image
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image
from PIL import Image

# Change to the path of your images folder
data_path = "data/images"

# Step 1: Initialize the Faster R-CNN model with the best available weights
weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
model = fasterrcnn_resnet50_fpn(weights=weights, box_score_thresh=0.9)
# Set the model to evaluation mode
model.eval()

# Step 2: Create a new folder to store the cropped images
cropped_path = "data/images/cropped"
if not os.path.exists(cropped_path):
    os.mkdir(cropped_path)

# Step 3: Iterate over all entries in the data folder
for entry in os.scandir(data_path):
    # Step 3a: If the entry is not a directory, process it
    if not entry.is_dir():
        # Read the image and convert it to a tensor
        img_tensor = read_image(entry.path)
        # Convert the tensor to a floating-point type
        img_tensor = img_tensor.to(dtype=torch.float32)
        # Step 3c: Use the Faster R-CNN model to get a prediction for the image
        prediction = model([img_tensor], targets=None)[0]
        
        # Step 3d: Draw bounding boxes around the animals in the image
        labels = [weights.meta["categories"][i] for i in prediction["labels"]]
        
        # Convert the tensor to the torch.uint8 type
        img_tensor = img_tensor.to(dtype=torch.uint8)
        
        box = draw_bounding_boxes(img_tensor, boxes=prediction["boxes"], labels=labels,
                                  colors="red", width=4, font_size=30)
        # Step 3e: Convert the image to a PIL Image
        with to_pil_image(box.detach()) as im:
            # Step 3f: Save the image to the cropped folder
            im.save(os.path.join(cropped_path, entry.name))
