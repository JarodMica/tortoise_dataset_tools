import os
import multiprocessing
import subprocess
import tkinter as tk
from tkinter import filedialog
import shutil

def process_file(file_path, output_dir):
    try:
        # Get file duration using ffprobe
        duration_output = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path])
        duration = float(duration_output.decode().strip())

        if duration > 21600:  # 6 hours in seconds
            # Split the file into two parts
            file_name, file_ext = os.path.splitext(os.path.basename(file_path))
            output_file1 = os.path.join(output_dir, 'split', f"{file_name}_part1{file_ext}")
            output_file2 = os.path.join(output_dir, 'split', f"{file_name}_part2{file_ext}")

            # Use ffmpeg to split the file
            split_time = duration / 2
            subprocess.call(['ffmpeg', '-i', file_path, '-t', str(split_time), '-c', 'copy', output_file1])
            subprocess.call(['ffmpeg', '-i', file_path, '-ss', str(split_time), '-c', 'copy', output_file2])

            # Move the original file to the "original" folder
            original_file = os.path.join(output_dir, 'original', os.path.basename(file_path))
            shutil.move(file_path, original_file)
        else:
            # Move the file to the "not_split" folder
            output_file = os.path.join(output_dir, 'not_split', os.path.basename(file_path))
            shutil.move(file_path, output_file)
    except subprocess.CalledProcessError as e:
        print(f"Error processing file: {file_path}")
        print(f"Error message: {e}")

def process_folder(folder_path):
    # Create "split", "original", and "not_split" folders if they don't exist
    split_folder = os.path.join(folder_path, 'split')
    original_folder = os.path.join(folder_path, 'original')
    not_split_folder = os.path.join(folder_path, 'not_split')
    os.makedirs(split_folder, exist_ok=True)
    os.makedirs(original_folder, exist_ok=True)
    os.makedirs(not_split_folder, exist_ok=True)

    # Get list of files in the folder
    file_list = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

    # Create a pool of processes
    pool = multiprocessing.Pool(processes=8)

    # Process each file in parallel
    pool.starmap(process_file, [(file, folder_path) for file in file_list])

    # Close the pool
    pool.close()
    pool.join()

if __name__ == '__main__':
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()

    # Ask the user to select a folder
    folder_path = filedialog.askdirectory(title="Select a folder to process")

    if folder_path:
        process_folder(folder_path)
        print("Processing complete.")
    else:
        print("No folder selected. Exiting.")