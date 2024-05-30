# Merge datasets in a way to make sure audio files are not the same name. Select the folder directly in ./training/

import os
import shutil
from tkinter import filedialog
from tkinter import Tk

def choose_folder(title):
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title=title)
    root.destroy()
    return folder

def check_dataset(dataset_path):
    if "train.txt" not in os.listdir(dataset_path):
        print("The chosen dataset is not a valid dataset to merge!")
        exit()

def create_directory(base_path, base_name):
    suffix = 0
    while True:
        new_dir_name = f"{base_name}{'' if suffix == 0 else f'_{suffix}'}"
        new_dir_path = os.path.join(base_path, new_dir_name)
        try:
            os.mkdir(new_dir_path)
            print(f"Directory created: {new_dir_path}")
            return new_dir_name
        except FileExistsError:
            suffix += 1

def merge_files(src_files, dest_file):
    with open(dest_file, "w", encoding="utf-8") as outfile:
        for fname in src_files:
            with open(fname, "r", encoding="utf-8") as infile:
                shutil.copyfileobj(infile, outfile) # Used because files are copied in whole, no modifications

def copy_audio_files(source_dir, target_dir):
    for audio_file in os.listdir(source_dir):
        shutil.copy2(os.path.join(source_dir, audio_file), target_dir)

def combine_datasets(dataset1_path, dataset2_path, base_dir="./training"):
    new_dir_name = create_directory(base_dir, "merged_datasets")
    new_dir_path = os.path.join(base_dir, new_dir_name)

    # Merging train.txt files
    merge_files([os.path.join(dataset1_path, "train.txt"), os.path.join(dataset2_path, "train.txt")],
                os.path.join(new_dir_path, "train.txt"))

    # Copying audio files
    audio_folder = "audio"
    merged_audio_path = os.path.join(new_dir_path, audio_folder)
    os.mkdir(merged_audio_path)
    copy_audio_files(os.path.join(dataset1_path, audio_folder), merged_audio_path)
    copy_audio_files(os.path.join(dataset2_path, audio_folder), merged_audio_path)

def main():
    dataset1_path = choose_folder(title="Choose Dataset 1")
    check_dataset(dataset1_path)
    dataset2_path = choose_folder(title="Choose Dataset 2")
    check_dataset(dataset2_path)
    combine_datasets(dataset1_path, dataset2_path)

if __name__ == "__main__":
    main()
