import os

# Define the dataset directory
dataset_dir = 'data/datasets/chess3'

# Derive paths to images and labels directories from dataset_dir
images_dir = os.path.join(dataset_dir, 'images')
labels_dir = os.path.join(dataset_dir, 'labels')

# Get a list of all label files (strip file extensions)
label_files = [os.path.splitext(filename)[0] for filename in os.listdir(labels_dir) if filename.endswith('.txt')]

# Iterate through the image files
for filename in os.listdir(images_dir):
    if filename.endswith('.JPG') or filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        # Strip the file extension to get the base filename
        base_filename = os.path.splitext(filename)[0]
        
        # Check if there is a corresponding label file for the image
        if base_filename not in label_files:
            # Construct the full path to the image file
            image_path = os.path.join(images_dir, filename)
            
            # Delete the image file
            os.remove(image_path)
            print(f"Deleted: {image_path}")
