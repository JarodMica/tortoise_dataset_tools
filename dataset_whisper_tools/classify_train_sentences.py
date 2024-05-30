# Classifies lines in a tortoise compatible train.txt file for the langauge of the sentence

import os
from tkinter import filedialog, Tk
from langdetect import detect
from multiprocessing import Pool

def choose_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

def detect_language(sentence):
    try:
        language = detect(sentence)
        return language
    except:
        pass

def process_line(line):
    valid_languages = ['en', 'vi', 'ja']
    audio_file, transcript = line.strip().split('|')
    language = detect_language(transcript)
    if language in valid_languages:
        updated_transcript = f"[{language}]{transcript}"
    else:
        updated_transcript = transcript
    return f"{audio_file}|{updated_transcript}\n"

def process_train_file(train_file_path, train_file_updated):
    with open(train_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    num_processes = os.cpu_count()
    with Pool(processes=num_processes) as pool:
        updated_lines = pool.map(process_line, lines)

    with open(train_file_updated, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)

def main():
    train_file_path = choose_file()
    train_file_updated = os.path.join(os.path.dirname(train_file_path), "train_lang.txt")
    process_train_file(train_file_path, train_file_updated)
    print(f"Updated train file saved as: {train_file_updated}")

if __name__ == "__main__":
    main()