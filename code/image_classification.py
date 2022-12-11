import os
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
from torchvision.io.image import read_image
from torchvision.utils import draw_bounding_boxes, save_image
from torchvision.transforms.functional import to_pil_image
from PIL import Image

# Change to the path of your images folder
data_path = "data/images"
# Make the file readable by everyone
os.chmod(data_path, 0o644)

# Step 1: Initialize the Faster R-CNN model with the best available weights
weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
model = fasterrcnn_resnet50_fpn(weights=weights, box_score_thresh=0.9)
# Set the model to evaluation mode
model.eval()

# Step 2: Create a new folder to store the cropped images
cropped_path = "data/images/cropped"
if not os.path.exists(cropped_path):
    os.mkdir(cropped_path)
    os.chmod(cropped_path, 0o644)

# Step 3: Iterate over all entries in the data folder
with os.scandir(data_path) as entries:
    for entry in entries:
        # Step 3a: If the entry is not a directory, process it
        if not entry.is_dir():
            # Step 3b: Read the image
            img = Image.open(entry.path)
            # Step 3c: Convert the image to a torch.Tensor object
            img_tensor = to_tensor(img)
            # Step 3d: Use the Faster R-CNN model to get a prediction for the image
            prediction = model([img_tensor], targets=None)[0]
            # Step 3e: Draw bounding boxes around the animals in the image
            labels = [weights.meta["categories"][i] for i in prediction["labels"]]
            box = draw_bounding_boxes(img, boxes=prediction["boxes"], labels=labels,
                                      colors="red", width=4, font_size=30)
            # Step 3f: Convert the image to a PIL Image
            im = to_pil_image(box.detach())
            # Step 3f: Save the image to the cropped folder
            im.save(os.path.join(cropped_path, entry.name))
            


