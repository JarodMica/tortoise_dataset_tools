# Adds tag to train.txt file based on folder name

import os
import tkinter as tk
from tkinter import filedialog

def add_special_token_to_sentences(folder_path, file_name='train.txt'):
    # Get the folder name
    folder_name = os.path.basename(folder_path.rstrip('/'))
    special_token = f"[{folder_name}]"

    # Construct the path to the train.txt file
    file_path = os.path.join(folder_path, file_name)

    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Add special token to each sentence
    modified_lines = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 2:
            modified_line = f"{parts[0]}|{special_token}{parts[1]}"
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)  # In case the line format is unexpected

    # Rename the original file to train_original.txt
    os.rename(file_path, os.path.join(folder_path, "train_original.txt"))

    # Write the modified content back to train.txt
    with open(file_path, 'w') as file:
        file.writelines(modified_lines)

    print(f"Modified file saved as {file_path}")

if __name__ == "__main__":
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select the folder
    folder_path = filedialog.askdirectory(title="Select Folder Containing train.txt")

    if folder_path:
        add_special_token_to_sentences(folder_path)
    else:
        print("No folder selected.")
