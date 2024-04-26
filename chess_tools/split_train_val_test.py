import os
import random
import shutil

def create_directory(directory):
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

def split_dataset(dataset_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    # Define paths to images and labels directories
    images_dir = os.path.join(dataset_dir, 'images')
    labels_dir = os.path.join(dataset_dir, 'labels')

    # Get list of image and label files
    image_files = [filename for filename in os.listdir(images_dir)]

    # Create train, val, and test directories under images and labels folders
    for folder in ['train', 'val', 'test']:
        create_directory(os.path.join(images_dir, folder))
        create_directory(os.path.join(labels_dir, folder))

    # Shuffle files randomly
    random.shuffle(image_files)

    # Calculate number of files for train, val, and test sets
    total_files = len(image_files)
    num_train = int(total_files * train_ratio)
    num_val = int(total_files * val_ratio)

    # Assign files to train, val, and test sets
    train_images = image_files[:num_train]
    val_images = image_files[num_train:num_train + num_val]
    test_images = image_files[num_train + num_val:]

    # Move images and labels to corresponding directories
    def move_image(file_list, src_dir, dest_dir):
        for filename in file_list:
            # Move image file
            src_image = os.path.join(src_dir, filename)
            dest_image = os.path.join(dest_dir, filename)
            shutil.move(src_image, dest_image)
    
    def move_label(file_list, src_dir, dest_dir):
        for filename in file_list:
            # Move label file
            base_filename = os.path.splitext(filename)[0]
            label_filename = f"{base_filename}.txt"
            src_label = os.path.join(src_dir, label_filename)
            dest_label = os.path.join(dest_dir, label_filename)
            shutil.move(src_label, dest_label)

    # Move files to train, val, and test directories under images and labels folders
    move_image(train_images, images_dir, os.path.join(images_dir, 'train'))
    move_label(train_images, labels_dir, os.path.join(labels_dir, 'train'))
    move_image(val_images, images_dir, os.path.join(images_dir, 'val'))
    move_label(val_images, labels_dir, os.path.join(labels_dir, 'val'))
    move_image(test_images, images_dir, os.path.join(images_dir, 'test'))
    move_label(test_images, labels_dir, os.path.join(labels_dir, 'test'))

    print("Images split and organized successfully!")

if __name__ == "__main__":
    dataset_dir = 'data/datasets/bbox-chess3'
    split_dataset(dataset_dir)
