'''
Romanizes a train.txt file meant for tortoise
'''

import tkinter as tk
from tkinter import filedialog
import cutlet

def convert_to_romaji(input_file, output_file):
    # Initialize Cutlet
    katsu = cutlet.Cutlet()
    katsu.use_foreign_spelling = False
    
    with open(input_file, 'r', encoding='utf-8') as file, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 2:
                # Convert to romaji
                romaji = katsu.romaji(parts[1])
                # Write to output file
                outfile.write(f"{parts[0]}|{romaji}\n")
            else:
                print(f"Invalid line format: {line}")

if __name__ == "__main__":
    # Set up the file dialog
    root = tk.Tk()
    root.withdraw()  # to hide the small tk window

    # Show an "Open" dialog box and return the path to the selected file
    input_file = filedialog.askopenfilename(title="Select input file", filetypes=[("Text files", "*.txt")])

    if input_file:
        output_file = 'output_data.txt'  # or ask the user for a filename
        convert_to_romaji(input_file, output_file)
        print(f"Conversion completed. Output file: {output_file}")
    else:
        print("File selection cancelled.")
