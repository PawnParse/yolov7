import os
import shutil

def create_directory(directory):
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

def add_new_data_to_train_split(dataset_from, dataset_to):
    # Define paths to images and labels directories
    images_to = os.path.join(dataset_to, 'images')
    labels_to = os.path.join(dataset_to, 'labels')
    images_from = os.path.join(dataset_from, 'images')
    labels_from = os.path.join(dataset_from, 'labels')

    # Create train, val, and test directories under images and labels folders
    for split in ['train', 'val', 'test']:
        create_directory(os.path.join(images_to, split))
        create_directory(os.path.join(labels_to, split))


    def get_existing_image_filenames(dir):
        # Get a set of existing image filenames in the directory
        return set(filename for filename in os.listdir(dir) if filename.endswith(('.jpg', '.png', '.jpeg')))

    # Get existing image filenames in the validation and test directories of the new dataset
    val_images_set = get_existing_image_filenames(os.path.join(images_to, 'val'))
    test_images_set = get_existing_image_filenames(os.path.join(images_to, 'test'))

    # Copy old validation and test images and labels to the train split of the new dataset
    def copy(split):
        # Copy old validation images and labels
        for filename in os.listdir(os.path.join(images_from, split)):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                # Copy image file
                src_image = os.path.join(images_from, split, filename)
                dest_image = os.path.join(images_to, split, filename)
                shutil.copy(src_image, dest_image)

                # Copy corresponding label file if it exists
                base_filename = os.path.splitext(filename)[0]
                label_filename = f"{base_filename}.txt"
                src_label = os.path.join(labels_from, split, label_filename)
                dest_label = os.path.join(labels_to, split, label_filename)
                if os.path.exists(src_label):
                    shutil.copy(src_label, dest_label)

    copy('val')
    copy('test')
    copy('train')

    # Copy new images and labels from the old dataset and new dataset to the train split
    def copy_images_to_train(split='train'):
        for filename in os.listdir(os.path.join(images_from, split)):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                # Check if image is not in val or test sets
                if filename not in val_images_set and filename not in test_images_set:
                    # Copy image file
                    src_image = os.path.join(images_to, split, filename)
                    dest_image = os.path.join(images_to, split, filename)
                    shutil.copy(src_image, dest_image)

                    # Copy corresponding label file if it exists
                    base_filename = os.path.splitext(filename)[0]
                    label_filename = f"{base_filename}.txt"
                    src_label = os.path.join(labels_from, split, label_filename)
                    dest_label = os.path.join(labels_to, split, label_filename)
                    if os.path.exists(src_label):
                        shutil.copy(src_label, dest_label)
            else:
                print(f"Skipping double file{filename}")

    # Copy new images and labels from the old dataset and new dataset to the train split
    # copy_images_to_train()

    print("Additional data added to train split successfully!")

if __name__ == "__main__":
    # Example usage:
    dataset_from = 'data/datasets/bbox-chess3'
    dataset_to = 'data/datasets/bbox5_prod_v1'

    # Add new data (excluding val and test images) and old val/test images to the train split
    add_new_data_to_train_split(dataset_from, dataset_to)