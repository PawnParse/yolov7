# This script converts all image files in the current directory to jpg files
# with PIL

import os
from pathlib import Path
import shutil

from PIL import Image

# Get the current directory
current_dir = Path.cwd()
# current_dir = Path('data/datasets/bbox-chess3/images/val')

for file in current_dir.iterdir():
    if file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.heic']:
        
        print(f"Converting {file.name} to jpg")
        img = Image.open(file)

        backup_file = file.with_name('backup_' + file.name)
        shutil.copy2(file, backup_file)

        # convert
        # delete alpha channel
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        jpg_file = file.with_suffix('.jpg')


        # save new, delete original
        file.unlink()
        img.save(jpg_file)
        # jpg_file.rename(file.name)

        # delete backup
        backup_file.unlink()
        print(f"Converted {file.name} to {jpg_file.name}")
