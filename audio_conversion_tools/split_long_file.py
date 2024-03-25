import os
import multiprocessing
import subprocess
import tkinter as tk
from tkinter import filedialog
import shutil
import math

def get_duration(file_path):
    try:
        # Get file duration using ffprobe
        duration_output = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path])
        duration = float(duration_output.decode().strip())
        return duration
    except subprocess.CalledProcessError as e:
        print(f"Error getting duration for file: {file_path}")
        print(f"Error message: {e}")
        return None

def process_file(file_path, output_dir):
    try:
        duration = get_duration(file_path)
        hours = 2
        if duration is not None:
            if duration > hours*3600:  # 4 hours in seconds
                # Calculate the number of parts needed
                num_parts = math.ceil(duration / (hours*3600))
                
                # Split the file into multiple parts
                file_name, file_ext = os.path.splitext(os.path.basename(file_path))
                split_time = duration / num_parts
                
                for i in range(num_parts):
                    start_time = i * split_time
                    output_file = os.path.join(output_dir, 'split', f"{file_name}_part{i+1}{file_ext}")
                    
                    if i == num_parts - 1:
                        # Last part, use the remaining duration
                        subprocess.call(['ffmpeg', '-i', file_path, '-ss', str(start_time), '-c', 'copy', output_file])
                    else:
                        # Split the file using the calculated split time
                        subprocess.call(['ffmpeg', '-i', file_path, '-ss', str(start_time), '-t', str(split_time), '-c', 'copy', output_file])
                
                # Move the original file to the "original" folder
                original_file = os.path.join(output_dir, 'original', os.path.basename(file_path))
                shutil.move(file_path, original_file)
            else:
                # Move the file to the "not_split" folder
                output_file = os.path.join(output_dir, 'not_split', os.path.basename(file_path))
                shutil.move(file_path, output_file)
    
    except Exception as e:
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
    
    # Merge "split" and "not_split" folders into "valid_splits"
    # valid_splits_folder = os.path.join(folder_path, 'valid_splits')
    # os.makedirs(valid_splits_folder, exist_ok=True)
    
    for folder in [split_folder, not_split_folder]:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            shutil.move(file_path, os.path.join(folder_path, file))
    
    # Remove the empty "split" and "not_split" folders
    os.rmdir(split_folder)
    os.rmdir(not_split_folder)

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