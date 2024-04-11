#!/bin/bash

# Create a temporary directory
mkdir temp

# Copy all files and directories from 'fine-tuning/' into 'temp/'
cp -rv ./* temp

# Change directory to 'temp'
cd temp

# Remove specific directories or files within 'temp'
rm -r data/datasets/
# Uncomment the following lines if you want to remove additional directories or files
# yes | rm -r .git
# rm -r .ipynb_checkpoints
rm -r models/*.pt
rm -r runs/
rm -r paper

# Zip the contents of 'temp' (but not the 'temp' directory itself) into 'fine-tune-code.zip'
zip -r ../yolov7.zip ./*

# Change back to the parent directory
cd ..

# Remove the 'temp' directory
rm -r temp