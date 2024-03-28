'''
This is meant to transcribe a folder containing lots of large files.  If you try to run it on a folder containing
lots of tiny files, operation time will take extremely long due to relying on subprocess calls to whisperx here.

A Python implementation of whisperx should be faster.
'''

import csv
import random
import subprocess
import pysrt
import shutil
from pydub import AudioSegment
from tqdm import tqdm 
import tkinter as tk
from tkinter import filedialog
from pathlib import Path  # Import the pathlib library
import tempfile
import multiprocessing
import os

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


def run_whisperx(audio_files, output_dir, language, chunk_size=20, no_align=False):
    cmd = ["whisperx", audio_files, 
        "--device", "cuda",
        "--model", "large-v3", 
        "--output_dir", output_dir, 
        "--language", f"{language}",
        "--chunk_size", f"{chunk_size}",
        # "--align_model", "Harveenchadha/vakyansh-wav2vec2-tamil-tam-250",
        "--output_format", "srt"]
    if no_align:
        cmd.append("--no_align") # It might be better to run with this parameter for languages w/o align model as some alignment models are not good)
    
    if language == "ja":
        chunk_size = 8
    try:
        subprocess.run(cmd, check=True )
    except Exception as e:
        print(f"Error in running whisperx for file {audio_files}: {e}")

def process_segment(sub, audio, audio_file, output_dir, padding, file_count, i):
    start_time = max(0, sub.start.ordinal - int(padding * 1000))
    end_time = min(sub.end.ordinal + int(padding * 1000), len(audio))
    base_name = audio_file.stem
    output_filename = f"{base_name}_segment_{file_count + i + 1}.mp3"
    output_path = output_dir / output_filename
    segment = audio[start_time:end_time]
    segment.export(output_path, format="mp3")
    print(f"Saved segment {i+1} to {output_path}")
    return output_filename, sub.text

def process_subtitles(subs, audio, audio_file, output_dir, padding, file_count):
    segment_details = []
    for i, sub in enumerate(subs):
        output_filename, sub_text = process_segment(sub, audio, audio_file, output_dir, padding, file_count, i)
        segment_details.append((output_filename, sub_text))
    return segment_details

def extract_audio_with_srt(audio_file, srt_file, output_dir, num_processes, padding=0.2):
    audio_file = Path(audio_file)  # Convert to Path object
    srt_file = Path(srt_file)  # Convert to Path object
    output_dir = Path(output_dir)  # Convert to Path object
    segment_details = []

    try:
        subs = pysrt.open(srt_file)
        output_dir.mkdir(parents=True, exist_ok=True)
        existing_files = list(output_dir.iterdir())
        file_count = len(existing_files)
        audio = AudioSegment.from_file(audio_file)
        audio = audio.set_frame_rate(22050)

        # Split subtitles into chunks of 8
        subtitle_chunks = [subs[i:i+8] for i in range(0, len(subs), 8)]

        with multiprocessing.Pool(processes=num_processes) as pool:
            results = [pool.apply_async(process_subtitles, args=(chunk, audio, audio_file, output_dir, padding, file_count + i*8))
                       for i, chunk in enumerate(subtitle_chunks)]
            for result in results:
                segment_details.extend(result.get())

    except Exception as e:
        print(f"Error processing file {audio_file} with SRT {srt_file}: {e}")

    return segment_details

def process_audio_files(base_directory, language, audio_dir, num_processes, chunk_size=20, no_align=False, rename_files=False):
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

    file_counter = 1  # Initialize the file counter

    with train_txt_path.open('a', encoding='utf-8') as train_file, \
         eval_txt_path.open('a', encoding='utf-8') as eval_file, \
         progress_log_path.open('a', encoding='utf-8') as log_file:

        all_files = []
        for file in os.listdir(audio_dir):
            if file.lower().endswith(('.wav', '.mp3', '.opus', '.webm', '.mp4')):
                file_path = os.path.join(audio_dir, file)
                all_files.append(Path(file_path))
        
        for audio_path in tqdm(all_files, desc="Processing audio files"):
            # Skip if already processed
            if str(audio_path) in processed_files:
                continue

            if rename_files:
                # Generate a new name for the file using the counter
                new_file_name = f"file___{file_counter}{audio_path.suffix}"
                new_audio_path = audio_path.with_name(new_file_name)
                # Create a copy of the audio file with the new name
                try:
                    shutil.copy(str(audio_path), str(new_audio_path))
                except FileNotFoundError:
                    print(f"File not found: {audio_path}. Skipping...")
                    continue
                file_counter += 1  # Increment the file counter
            else:
                new_audio_path = audio_path

            relative_path = new_audio_path.relative_to(audio_dir)
            srt_output_dir = split_output_dir / relative_path.with_suffix('')
            srt_file = srt_output_dir / (relative_path.stem + '.srt')

            srt_output_dir.mkdir(parents=True, exist_ok=True)

            if not srt_file.exists():
                run_whisperx(new_audio_path, srt_output_dir, language, chunk_size, no_align)
                
            if len(os.listdir(srt_output_dir)) > 1:
                new_audio_path.unlink()
                continue
            else:
                segment_details = extract_audio_with_srt(new_audio_path, srt_file, srt_output_dir, num_processes)

            for segment_file, text in segment_details:
                segment_path = srt_output_dir / segment_file
                csv_entry_path = f"audio/{segment_path.relative_to(split_output_dir).as_posix().replace('/', '_')}"
                entry = f"{csv_entry_path}|{text}\n"

                if random.random() < 0.05:
                    eval_file.write(entry)
                else:
                    train_file.write(entry)

            # Delete the renamed file after transcription
            if rename_files:
                new_audio_path.unlink()

            # Log the original file path
            log_file.write(f"{str(audio_path)}\n")
            log_file.flush()  # Ensure it's written immediately

def main():
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
    process_audio_files(base_directory=finetune_dir, model_name='large-v3', language=language, batch_size=16, speaker_name='coqui', audio_dir=chosen_directory)

if __name__ == "__main__":
    main()