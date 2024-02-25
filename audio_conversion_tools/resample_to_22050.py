import os
import subprocess
import tkinter as tk
from tkinter import filedialog
import multiprocessing

def convert_audio(input_files, output_folder):
    for input_file in input_files:
        output_file = os.path.join(output_folder, os.path.basename(input_file))
        ffmpeg_command = f'ffmpeg -i "{input_file}" -ar 22050 "{output_file}"'
        subprocess.run(ffmpeg_command, shell=True)

def process_folder(input_folder):
    output_folder = os.path.join(input_folder, "resampled")

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.mp3')]  # Modify the extension as needed
    num_cores = multiprocessing.cpu_count()

    # Split input_files into chunks for parallel processing
    chunk_size = len(input_files) // num_cores
    input_file_chunks = [input_files[i:i + chunk_size] for i in range(0, len(input_files), chunk_size)]

    with multiprocessing.Pool(num_cores) as pool:
        pool.starmap(convert_audio, [(input_file_chunk, output_folder) for input_file_chunk in input_file_chunks])

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    input_folder = filedialog.askdirectory(title="Select Input Folder")
    if not input_folder:
        return  # User canceled folder selection

    process_folder(input_folder)

if __name__ == "__main__":
    main()
