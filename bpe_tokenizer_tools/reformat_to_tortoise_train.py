'''
This script is specific to the converting datasets formated in this style: 

audiopath | raw transcript | normalized transcript | speaker ID

This script will take audiopath and normalized transcript and reformat the train file to be:

audiopath | normalized transcript

However, it's slightly unique in that it also changes the path to look for the training file
to audio.  For example, the following will be converted to the format:

some_other_folder/audio_sample.mp3 | normalized transcript --> audio/audio_sample.mp3 | normalized transcript

As tortoise defaults to audio as the folder name containing the audio training data. In reality, it
shoudn't matter too much as you can keep the folder name if you'd like, you would just need to make
sure that the path is correct for tortoise to look for. 
'''

import os
import tkinter as tk
from tkinter import filedialog

def process_line(line):
    parts = line.strip().split('|')
    parts[0] = 'audio/' + parts[0].split('/')[1]
    return f"{parts[0]}|{parts[2]}"

def select_input_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select Input Text File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    return file_path

def main():
    input_file_path = select_input_file()
    if not input_file_path:
        print("No file selected. Exiting...")
        return
    
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the output file path in the same directory as the script
    output_file_path = os.path.join(script_dir, 'train.txt')
    
    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            processed_line = process_line(line)
            outfile.write(processed_line + '\n')
    
    print("File processing completed.")

if __name__ == "__main__":
    main()

