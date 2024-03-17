import os
import tkinter as tk
from tkinter import filedialog
from multiprocessing import Pool, cpu_count
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def convert_audio(input_file, output_folder):
    output_file = os.path.join(output_folder, os.path.basename(input_file))
    if not os.path.exists(output_file):
        try:
            audio = AudioSegment.from_file(input_file)
            audio = audio.set_frame_rate(22050)
            audio.export(output_file, format="mp3")
        except CouldntDecodeError as e:
            print(f"Error processing {input_file}: {e}. Skipping this file.")
        except Exception as e:
            print(f"Unexpected error with {input_file}: {e}. Skipping this file.")
    else:
        print(f"Skipping {os.path.basename(input_file)} as it already exists in {output_folder}")

def process_files(input_files, output_folder):
    for input_file in input_files:
        convert_audio(input_file, output_folder)

def process_folder(input_folder):
    output_folder = os.path.join(input_folder, "resampled")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.opus')]
    files_per_process = max(len(input_files) // cpu_count(), 1)  # Ensure at least 1 file per process

    # Divide the work among available CPUs
    file_chunks = [input_files[i:i + files_per_process] for i in range(0, len(input_files), files_per_process)]

    with Pool() as pool:
        pool.starmap(process_files, [(chunk, output_folder) for chunk in file_chunks])

def main():
    root = tk.Tk()
    root.withdraw()
    input_folder = filedialog.askdirectory(title="Select Input Folder")
    if not input_folder:
        return
    process_folder(input_folder)

if __name__ == "__main__":
    main()
