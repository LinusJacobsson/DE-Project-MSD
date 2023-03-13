# Script that goes through the subset and puts all .h5-files in one directory
# Written by Linus Jacobsson March 13 2023 
import os
import shutil

root_dir = '/path/to/root/folder'
new_dir = '/path/to/new/folder'

# Loop through all subdirectories
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Loop through all files in the directory
    for filename in filenames:
        # Check if file is an h5 file
        if filename.endswith('.h5'):
            # Create new directory if it doesn't exist
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            # Copy file to new directory
            shutil.copy(os.path.join(dirpath, filename), new_dir)

