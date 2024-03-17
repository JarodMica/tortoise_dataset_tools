'''
This is meant to transcribe a folder containing lots of large files.  If you try to run it on a folder containing
lots of tiny files, operation time will take extremely long due to relying on subprocess calls to whisperx here.

A Python implementation of whisperx should be faster.
'''

import csv
import random
import subprocess
import pysrt
from pydub import AudioSegment
from tqdm import tqdm 
import tkinter as tk
from tkinter import filedialog
from pathlib import Path  # Import the pathlib library

def create_unique_directory(base_dir):
    """
    Create a unique directory by adding a suffix if the directory already exists.
    """
    suffix = 0
    base_dir = Path(base_dir)  # Convert to Path object
    dir_name = base_dir
    while dir_name.exists():
        suffix += 1
        dir_name = base_dir.parent / f"{base_dir.name}_{suffix}"  # Corrected line
    dir_name.mkdir(parents=True, exist_ok=True)  # Create the directory and parents if necessary
    return dir_name


def select_directory(title="Select Folder"):
    """
    Open a dialog to select a directory.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory(title=title)
    root.destroy()
    return Path(folder_selected)  # Convert to Path object


def run_whisperx(audio_files, output_dir, language):
    if language == "ja":
        chunk_size = 8
    elif language =="ta":
        chunk_size = 20
    else:
        chunk_size = 20
    try:
        subprocess.run(["whisperx", audio_files, 
                        "--device", "cuda",
                        "--model", "large-v3", 
                        "--output_dir", output_dir, 
                        "--language", f"{language}",
                        "--chunk_size", f"{chunk_size}",
                        # "--align_model", "Harveenchadha/vakyansh-wav2vec2-tamil-tam-250",
                        "--no_align", # It might be better to run with this parameter for languages w/o align model as some alignment models are not good
                        "--output_format", "srt"], check=True)
    except Exception as e:
        print(f"Error in running whisperx for file {audio_files}: {e}")

def extract_audio_with_srt(audio_file, srt_file, output_dir, padding=0.2):
    audio_file = Path(audio_file)  # Convert to Path object
    srt_file = Path(srt_file)  # Convert to Path object
    output_dir = Path(output_dir)  # Convert to Path object
    segment_details = []
    try:
        audio = AudioSegment.from_file(audio_file)
        subs = pysrt.open(srt_file)
        output_dir.mkdir(parents=True, exist_ok=True)

        existing_files = list(output_dir.iterdir())
        file_count = len(existing_files)

        for i, sub in enumerate(subs):
            start_time = max(0, sub.start.ordinal - int(padding * 1000))
            end_time = min(len(audio), sub.end.ordinal + int(padding * 1000))
            segment = audio[start_time:end_time]

            base_name = audio_file.stem
            output_filename = f"{base_name}_segment_{file_count + i + 1}.mp3"
            output_path = output_dir / output_filename
            segment.export(output_path, format="mp3")

            segment_details.append((output_filename, sub.text))
            print(f"Saved segment {i+1} to {output_path}")
    except Exception as e:
        print(f"Error processing file {audio_file} with SRT {srt_file}: {e}")
    return segment_details

def process_audio_files(base_directory, model_name, language, batch_size, speaker_name, audio_dir):
    base_directory = Path(base_directory)
    audio_dir = Path(audio_dir)

    train_txt_path = base_directory / 'dataset' / 'train.txt'
    eval_txt_path = base_directory / 'dataset' / 'validation.txt'
    split_output_dir = base_directory / 'dataset' / 'wav_splits'
    progress_log_path = base_directory / 'progress_log.txt'

    # Ensure the directories for the txt and log files exist
    train_txt_path.parent.mkdir(parents=True, exist_ok=True)
    progress_log_path.parent.mkdir(parents=True, exist_ok=True)

    # Load the set of already processed files
    if progress_log_path.exists():
        with progress_log_path.open('r', encoding='utf-8') as log_file:
            processed_files = {line.strip() for line in log_file}
    else:
        processed_files = set()

    with train_txt_path.open('a', encoding='utf-8') as train_file, \
         eval_txt_path.open('a', encoding='utf-8') as eval_file, \
         progress_log_path.open('a', encoding='utf-8') as log_file:

        all_files = [file for file in audio_dir.rglob('*') if file.suffix in ('.wav', '.mp3', '.opus')]

        for audio_path in tqdm(all_files, desc="Processing audio files"):
            # Skip if already processed
            if str(audio_path) in processed_files:
                continue

            relative_path = audio_path.relative_to(audio_dir)
            srt_output_dir = split_output_dir / relative_path.with_suffix('')
            srt_file = srt_output_dir / (relative_path.stem + '.srt')

            srt_output_dir.mkdir(parents=True, exist_ok=True)

            if not srt_file.exists():
                run_whisperx(str(audio_path), str(srt_output_dir), language)
            
            segment_details = extract_audio_with_srt(str(audio_path), str(srt_file), str(srt_output_dir))

            for segment_file, text in segment_details:
                segment_path = srt_output_dir / segment_file
                csv_entry_path = f"audio/{segment_path.relative_to(split_output_dir).as_posix().replace('/', '_')}"
                entry = f"{csv_entry_path}|{text}\n"

                if random.random() < 0.05:
                    eval_file.write(entry)
                else:
                    train_file.write(entry)

            # Log the processed file
            log_file.write(f"{str(audio_path)}\n")
            log_file.flush()  # Ensure it's written immediately

if __name__ == "__main__":
    tortoise_base_dir = Path('tortoise_data')
    finetune_base = tortoise_base_dir / 'finetune_models'
    
    # Ask user if they want to start new or continue existing
    action = input("Start new project (n) or continue existing project (c)? (n/c): ").strip().lower()
    
    if action == 'c':
        print("Please select the existing project directory you wish to continue.")
        finetune_dir = select_directory("Select Existing Project Directory")
        if not finetune_dir or not finetune_dir.exists():
            print("No valid directory selected. Exiting.")
            exit()
        # Optional: You could check here if the selected directory is valid for continuation.
    else:
        print("Creating a new project directory.")
        finetune_dir = create_unique_directory(finetune_base)

    chosen_directory = select_directory("Select Folder with Audio Data")
    if not chosen_directory:
        print("No folder selected for audio data. Exiting.")
        exit()

    language = "de"
    process_audio_files(finetune_dir, model_name='large-v3', language=language, batch_size=16, speaker_name='coqui', audio_dir=chosen_directory)
