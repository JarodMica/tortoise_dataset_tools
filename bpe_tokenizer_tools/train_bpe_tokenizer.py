from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
import json
import os
import re
import tkinter as tk
from tkinter import filedialog

def clean_text(input_file_path, output_file_path):
    # Define the pattern to match numbers, specific symbols, and new lines
    # add \d to match any digit, and | is used to specify alternatives
    pattern = r'|�|«|\$|\n'

    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        text = input_file.read()
        cleaned_text = re.sub(pattern, '', text)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(cleaned_text)

def main():
    root = tk.Tk()
    root.withdraw()
    input_path = filedialog.askopenfilename(title="Select your input text file")
    if not input_path:
        print("No file selected. Exiting.")
        return

    current_dir = os.path.dirname(os.path.realpath(__file__))
    input_file_name = os.path.basename(input_path)
    cleaned_input_path = os.path.join(current_dir, f"cleaned_{input_file_name}")

    # Clean the input file
    clean_text(input_path, cleaned_input_path)

    # Initialize and train the tokenizer
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    trainer = BpeTrainer(special_tokens=["[STOP]", "[UNK]", "[SPACE]", "0","1","2","3","4","5","6","7","8","9"], vocab_size=256)
    tokenizer.train([cleaned_input_path], trainer)

    # Save the tokenizer
    tokenizer_path = os.path.join(current_dir, "new_tokenizer.json")
    tokenizer.save(tokenizer_path)

    # Load, update, and save the tokenizer configuration
    with open(tokenizer_path, 'r', encoding='utf-8') as f:
        tokenizer_json = json.load(f)
    tokenizer_json['model']['language'] = 'es'
    with open(tokenizer_path, 'w', encoding='utf-8') as f:
        json.dump(tokenizer_json, f, ensure_ascii=False, indent=4)

    print("Processing complete. Tokenizer saved to:", tokenizer_path)

if __name__ == "__main__":
    main()
