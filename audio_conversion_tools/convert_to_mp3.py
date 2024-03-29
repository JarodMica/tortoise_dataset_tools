import os
import shutil
import tkinter as tk
from tkinter import filedialog
import multiprocessing
from pydub import AudioSegment

def convert_audio_to_mp3(source_path, mp3_path):
    try:
        import time
        start = time.time()
        audio = AudioSegment.from_file(source_path)
        end = time.time()
        total_elapsed_time = end - start
        print(total_elapsed_time)
        audio.export(mp3_path, format="mp3", bitrate="320k", parameters=["-ar", "22050"])
        print(f"Converted {source_path} to {mp3_path}")
    except Exception as e:
        print(f"Error converting {source_path}: {e}")

def process_file(args):
    source_path, converted_folder = args
    file_name = os.path.basename(source_path)
    mp3_path = os.path.join(converted_folder, file_name.rsplit('.', 1)[0] + ".mp3")
    if file_name.lower().endswith(".mp3"):
        shutil.copy2(source_path, mp3_path)
        print(f"Copied {source_path} to {mp3_path}")
    else:
        convert_audio_to_mp3(source_path, mp3_path)

def process_folder(folder_path, num_processes):
    converted_folder = os.path.join(folder_path, "converted")
    if not os.path.exists(converted_folder):
        os.makedirs(converted_folder)
    
    audio_extensions = ["wav", "opus", "m4a", "webm", "mp3", "mp4"]
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.split('.')[-1] in audio_extensions]
    
    pool = multiprocessing.Pool(processes=num_processes)
    pool.map(process_file, [(file, converted_folder) for file in files])
    pool.close()
    pool.join()

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Folder")
    return folder_selected

if __name__ == "__main__":
    folder_path = select_folder()
    if folder_path:
        num_processes = multiprocessing.cpu_count()  # Use the number of CPU cores
        process_folder(folder_path, num_processes)
    else:
        print("No folder selected. Exiting...")