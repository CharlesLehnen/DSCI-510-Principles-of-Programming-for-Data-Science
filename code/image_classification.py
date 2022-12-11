import os
from torchvision.io.image import read_image
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image

# Directory containing images to process
image_dir = "data/images"

# Directory to save the cropped images
cropped_dir = os.path.join(image_dir, "cropped")

# Create the cropped directory if it doesn't exist
if not os.path.exists(cropped_dir):
    os.makedirs(cropped_dir)

# Step 1: Initialize model with the best available weights
weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
model = fasterrcnn_resnet50_fpn_v2(weights=weights, box_score_thresh=0.9)
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
