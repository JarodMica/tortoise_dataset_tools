'''
This script renames the files in the "audio" folder and "train.txt" files.

This is needed if you want to merge two datasets together. For example, if you DID NOT keep the original name of
the audio files, if you try to copy and paste between two datasets, you will be using the same name for files and
this conflict won't allow you to train, so you need to rename them to unique files AND THEN merge the datasets.
'''

import os
from tkinter import filedialog
from tkinter import Tk

def choose_folder():
    root = Tk() 
    root.withdraw()
    folder = filedialog.askdirectory()
    root.destroy() 
    return folder

def change_name(audio_file_path, new_name):
    audio_root_path = os.path.split(audio_file_path)[0]
    audio_ext = os.path.basename(audio_file_path).split(".")[1]
    new_name_path = os.path.join(audio_root_path, f'{new_name}.{audio_ext}')
    os.rename(audio_file_path, new_name_path)
    return new_name_path 

def main():
    folder_path = choose_folder()
    if folder_path:
        basename_change = os.path.basename(folder_path)
        if "train.txt" in os.listdir(folder_path):
            train_path = os.path.join(folder_path, "train.txt")
            updated_lines = [] 
            with open(train_path, "r", encoding="utf-8") as file:
                lines = file.readlines() 

            suffix = 1
            for line in lines:
                if line.strip():
                    original_line = line.strip()
                    name_to_change = original_line.split("|")[0].split("/")[-1]
                    new_name = f"{basename_change}_{suffix}"
                    audio_file_path = os.path.join(folder_path, "audio", name_to_change)
                    new_file_path = change_name(audio_file_path, new_name)
                    new_line = original_line.replace(name_to_change, os.path.basename(new_file_path)) + '\n'
                    updated_lines.append(new_line)
                    suffix += 1

            # Write the updated lines back to the file
            with open(train_path, "w", encoding="utf-8") as file:
                file.writelines(updated_lines)
        else:
            print("No train.txt found. Please select a directory that contains it.")
            exit() 
    else:
        print("No folder selected.")

if __name__ == "__main__":
    main()
