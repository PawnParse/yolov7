import os
from PIL import Image

def rotate_landscape_images(dataset_path):
    for filename in os.listdir(dataset_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(dataset_path, filename)
            with Image.open(file_path) as img:
                if img.width > img.height:
                    rotated_img = img.rotate(90, expand=True)
                    rotated_img.save(file_path)
                    print(f"Rotated {filename}")

if __name__ == "__main__":
    bbox5_dataset_path = "/path/to/bbox5/dataset"  # Replace with actual path
    rotate_landscape_images(bbox5_dataset_path)
