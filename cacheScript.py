import shutil
import os
import time
from datetime import datetime

def copy_files(source_folder, destination_folder):
    # Get a list of all files in the source folder
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    # Copy each file to the destination folder
    for file in files:
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)
        shutil.copy2(source_path, destination_path)  # Use shutil.copy2 to preserve metadata

# Specify source and destination folder paths
source_folder_path = 'output'  # Update with your actual source folder path
destination_folder_path = 'cache_output'  # Update with your desired destination folder path

# Infinite loop to periodically copy files
while True:
    # Generate a timestamp to create a unique subfolder name in the destination folder
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    subfolder_path = os.path.join(destination_folder_path, f"copied_files_{timestamp}")

    # Create the subfolder in the destination folder
    os.makedirs(subfolder_path)

    # Copy files from the source folder to the subfolder in the destination folder
    copy_files(source_folder_path, subfolder_path)

    # Print a message (optional)
    print(f"Files copied to: {subfolder_path}")

    # Wait for a specific duration (e.g., 1 hour)
    time.sleep(900)  # 3600 seconds = 1 hour
