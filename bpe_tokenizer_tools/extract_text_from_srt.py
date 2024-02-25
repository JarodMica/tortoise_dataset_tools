'''
Used to extract the words from an SRT file and put them into a combined text file.
Not used in the tokenizer workflow, but can be useful IF you want to take the text
from an srt file, a possible output of whisperx
'''

import os
import glob
import re
from tkinter import Tk, filedialog

def extract_text_from_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Remove any text inside brackets (e.g., for sound descriptions)
        content = re.sub(r"\[.*?\]", '', content)
        # Remove numeric indicators of subtitles and timestamps
        content = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', '', content)
        # Remove new lines and extra spaces
        content = re.sub(r'\n+', '', content).strip()
        return content

def main():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory() 
    srt_files = glob.glob(os.path.join(folder_selected, '*.srt'))
    all_text = []

    for file_path in srt_files:
        extracted_text = extract_text_from_srt(file_path)
        all_text.append(extracted_text)

    # Combine all texts and write to words.txt in the same folder
    with open(os.path.join(folder_selected, 'words.txt'), 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(all_text))

if __name__ == '__main__':
    main()
