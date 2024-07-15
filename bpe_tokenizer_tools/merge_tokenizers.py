'''
Merge two tokenizers together... Did not end up using this.  Script will need some cleaning and modification I think.
'''

from tkinter import filedialog
import tkinter as tk
import json
import shutil
import os

def merge_tokenizers(tokenizer1, tokenizer2):
    vocab1 = tokenizer1["model"]["vocab"]
    merges1 = tokenizer1["model"]["merges"]
    vocab2 = tokenizer2["model"]["vocab"]
    merges2 = tokenizer2["model"]["merges"]

    # Combine vocabularies
    start_index = max(vocab1.values()) + 1
    combined_vocab = vocab1.copy()
    for token, index in vocab2.items():
        if token not in combined_vocab:
            combined_vocab[token] = start_index
            start_index += 1

    # Combine merges
    combined_merges = merges1 + merges2

    # Update the tokenizer with the new combined vocab and merges
    tokenizer1["model"]["vocab"] = combined_vocab
    tokenizer1["model"]["merges"] = combined_merges

    return tokenizer1

def file_selection_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select tokenizer JSON file", filetypes=[("JSON files", "*.json")])
    return file_path

def main():
    original_tokenizer_path = file_selection_dialog()
    second_tokenizer_path = file_selection_dialog()

    with open(original_tokenizer_path, "r", encoding="utf-8") as file:
        tokenizer1 = json.load(file)
    
    with open(second_tokenizer_path, "r", encoding="utf-8") as file:
        tokenizer2 = json.load(file)

    combined_tokenizer = merge_tokenizers(tokenizer1, tokenizer2)

    # Save the combined tokenizer to a new JSON file
    output_path = os.path.join(os.path.dirname(original_tokenizer_path), "combined_tokenizer.json")
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(combined_tokenizer, file, ensure_ascii=False, indent=4)

    print(f"Combined tokenizer written to {output_path}")

if __name__ == "__main__":
    main()
