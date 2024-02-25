'''
Takes audio files and converts them to mp3 files sampled at 22050hz.
22050 hz is needed for Tortoise TTS which is why it's chosen
'''

import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
import multiprocessing


def convert_audio_to_mp3(source_path, mp3_path):
    try:
        cmd = ['ffmpeg', '-i', source_path, '-vn', '-ab', '320k', '-ar', '22050', '-y', mp3_path]
        subprocess.run(cmd, check=True)
        print(f"Converted {source_path} to {mp3_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {source_path}: {e}")

def process_folder(folder_path):
    converted_folder = os.path.join(folder_path, "converted")
    if not os.path.exists(converted_folder):
        os.makedirs(converted_folder)

    audio_extensions = ["wav", "opus", "m4a"]
    files = [f for f in os.listdir(folder_path) if f.split('.')[-1] in audio_extensions]

    # Utilize maximum CPU threads
    cpu_count = multiprocessing.cpu_count()

    with ThreadPoolExecutor(max_workers=cpu_count) as executor:
        for file_name in files:
            source_path = os.path.join(folder_path, file_name)
            mp3_path = os.path.join(converted_folder, file_name.rsplit('.', 1)[0] + ".mp3")
            executor.submit(convert_audio_to_mp3, source_path, mp3_path)

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory(title="Select Folder")
    return folder_selected

if __name__ == "__main__":
    folder_path = select_folder()
    if folder_path:
        process_folder(folder_path)
    else:
        print("No folder selected. Exiting...")
