'''
Extracts the second segment of a tortoise train.txt file and puts it into a text file.

This should work on any tortoise train.txt file since its path|transcript format.
'''

import os
import tkinter as tk
from tkinter import filedialog

def select_input_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select Input Text File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    return file_path

def extract_transcripts(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
            line_count, extracted_count = 0, 0
            for line in infile:
                line_count += 1
                parts = line.strip().split('|')
                # Change the condition to check for at least two parts
                if len(parts) >= 2:
                    transcript = parts[1].lower()  # Extract the transcript part
                    outfile.write(transcript + '\n')
                    extracted_count += 1
            print(f"Processed {line_count} lines and extracted {extracted_count} transcripts.")
            if line_count == 0:
                print("Warning: The input file is empty or does not exist.")
            elif extracted_count == 0:
                print("Warning: No transcripts were extracted. Check the format of your input file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__": 
    input_file = select_input_file()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(script_dir, 'bpe_train_text.txt')
    extract_transcripts(input_file, output_file_path)

    print("Transcripts have been extracted and saved to:", output_file_path)
