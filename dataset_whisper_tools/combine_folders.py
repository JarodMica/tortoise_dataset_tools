'''
Crawls through all folders in a chosen directory, find all audio segments, and then put them in one folder.

The folder structure should look like this:

Chosen directory/
├── folder1/
│   └── segments/
├── folder2/
│   └── segments/ 
├── folder3/
│   └── segments/
...
└── combined_folder/  # All segments from folder1/, folder2/, folder3/, etc. are moved here

This was a quick script made to combine the segments outputted from the extraction script as they're individual
folders inside dataset/wav_splits.
'''

import os
import shutil
import tkinter as tk
from tkinter import filedialog

def merge_segments(output_dir):
    combined_dir = os.path.join(output_dir, "audio")
    os.makedirs(combined_dir, exist_ok=True)

    for folder_name in os.listdir(output_dir):
        folder_path = os.path.join(output_dir, folder_name)
        if not os.path.isdir(folder_path) or folder_name == "audio":
            continue

        for segment_name in os.listdir(folder_path):
            if segment_name.endswith('.srt'):
                segment_path = os.path.join(folder_path, segment_name)
                os.remove(segment_path)
            else:    
                segment_path = os.path.join(folder_path, segment_name)
                new_segment_name = f"{folder_name}_{segment_name}"
                new_segment_path = os.path.join(combined_dir, new_segment_name)
                shutil.move(segment_path, new_segment_path)

        os.rmdir(folder_path)  # Remove the original directory after all its segments have been moved

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory_path = filedialog.askdirectory(title="Select Directory")
    return directory_path

if __name__ == "__main__":
    directory_path = select_directory()
    if directory_path:
        merge_segments(directory_path)
    else:
        print("No directory selected. Exiting...")