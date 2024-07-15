# for styleTTS

import tkinter as tk
from tkinter import filedialog, simpledialog
import os
from phonemizer import phonemize
from phonemizer.separator import Separator

def text_to_ipa(text, language='en-us'):
    ipa_text = phonemize(
        text,
        language=language,
        backend="espeak",
        preserve_punctuation=True,
        with_stress=True,
    )
    return ipa_text

def process_file(input_file_path, output_file_path, option, language='en-us'):
    with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            parts = line.strip().split('|')
            if len(parts) == 3:
                audio_path, text, number = parts
                if option == 'phonemize':
                    ipa_text = text_to_ipa(text, language)
                    output_file.write(f"{audio_path}|{ipa_text}|{number}\n")
                elif option == 'basename':
                    basename = os.path.basename(audio_path)
                    output_file.write(f"{basename}|{text}|{number}\n")
                elif option == 'both':
                    ipa_text = text_to_ipa(text, language)
                    basename = os.path.basename(audio_path)
                    output_file.write(f"{basename}|{ipa_text}|{number}\n")

def main():
    # Create Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog to select input file
    input_file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Text Files", "*.txt")])
    if not input_file_path:
        print("No file selected. Exiting...")
        return

    # Define the output file path
    output_file_path = filedialog.asksaveasfilename(title="Save Output File As", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if not output_file_path:
        print("No output file specified. Exiting...")
        return

    # Ask the user for the processing option
    option = simpledialog.askstring("Select Option", "Enter 'phonemize' to phonemize the text, 'basename' to keep the basename of the path, or 'both' to do both:")
    if option not in ['phonemize', 'basename', 'both']:
        print("Invalid option selected. Exiting...")
        return

    # Process the file
    process_file(input_file_path, output_file_path, option)

    print(f"Processing completed. Output saved to: {output_file_path}")

if __name__ == "__main__":
    main()
