from pathlib import Path
import random
import shutil

def create_directory(directory):
    # Create directory if it doesn't exist
    directory.mkdir(parents=True, exist_ok=True)

def split_dataset(dataset_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, write=False):
    dataset_path = Path(dataset_dir)
    images_dir = dataset_path / 'images'
    labels_dir = dataset_path / 'labels'

    # Get list of image files
    image_files = []
    for suffix in ['*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png']:
        image_files.extend(images_dir.glob(suffix))

    # Create train, val, and test directories under images and labels folders
    if write:
        for folder in ['train', 'val', 'test']:
            create_directory(images_dir / folder)
            create_directory(labels_dir / folder)

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

    def move_files(file_list, src_dir, dest_dir, extension=''):
        for file_path in file_list:
            if extension != '':
                file_path = file_path.with_suffix(extension)
            src_path = src_dir / file_path.name
            dest_path = dest_dir / file_path.name
            if write:
                shutil.move(src_path, dest_path)
            else:
                print(f'mock: mv {src_path}, {dest_path})')

    # Move files to train, val, and test directories under images and labels folders
    move_files(train_images, images_dir, images_dir / 'train')
    move_files(train_images, labels_dir, labels_dir / 'train', extension='.txt')
    move_files(val_images, images_dir, images_dir / 'val')
    move_files(val_images, labels_dir, labels_dir / 'val', extension='.txt')
    move_files(test_images, images_dir, images_dir / 'test')
    move_files(test_images, labels_dir, labels_dir / 'test', extension='.txt')
    if (labels_dir / 'rotation').exists():
        print('move rotation labels')
        if write:
            for folder in ['train', 'val', 'test']:
                create_directory(labels_dir / folder / 'rotation')
        move_files(train_images, labels_dir / 'rotation', labels_dir / 'train' / 'rotation', extension='.txt')
        move_files(val_images, labels_dir / 'rotation', labels_dir / 'val' / 'rotation', extension='.txt')
        move_files(test_images, labels_dir / 'rotation', labels_dir / 'test' / 'rotation', extension='.txt')

    print("Images split and organized successfully!")

if __name__ == "__main__":
    dataset_dir = 'data/datasets/bbox5_prod_v1'
    split_dataset(dataset_dir, write=True, train_ratio=0.98, val_ratio=0.01)
