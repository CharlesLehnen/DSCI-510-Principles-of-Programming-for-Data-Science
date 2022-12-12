import os
import random

# Folder containing images to process
image_dir = "data/images"

# Folder for cropped images
cropped_dir = os.path.join(image_dir, "cropped")


def classify_and_crop(image_dir, cropped_dir):  
    
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
            
    # Return the training, validation, and test filenames
    return train_filenames, valid_filenames, test_filenames

    print("test")

            
# Ask the user if they want to run the function
should_run = input("Do you want to run the classify_and_crop function? (y/n)")

# Check the user's response and run the function if they want to
if should_run.lower() == "y":
    # Call the classify_and_crop function and store the returned values in local variables
    train_filenames, valid_filenames, test_filenames = classify_and_crop(image_dir, cropped_dir)
else:
    print("The classify_and_crop function will not be run at this time.")

# Print the training, validation, and test filenames
print(f'Training filenames: {train_filenames}', f'Validation filenames: {valid_filenames}', f'Test filenames: {test_filenames}')
