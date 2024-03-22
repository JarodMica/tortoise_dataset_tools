from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
import json
import re

def clean_text(input_file_path, output_file_path):
    # Define the pattern to match numbers, specific symbols, and new lines
    # add \d to match any digit, and | is used to specify alternatives
    pattern = r'|�|«|\$|\n'

    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        text = input_file.read()
        cleaned_text = re.sub(pattern, '', text)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(cleaned_text)

def train_tokenizer(input_path, tokenizer_path, language):
    # Initialize a tokenizer with the BPE model
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    # Use a basic whitespace pre-tokenizer
    tokenizer.pre_tokenizer = Whitespace()

    trainer = BpeTrainer(special_tokens=["[STOP]", "[UNK]", "[SPACE]", "0","1","2","3","4","5","6","7","8","9",], vocab_size=256)

    clean_text(input_path, input_path)
    tokenizer.train([input_path], trainer)

    tokenizer.save(tokenizer_path)

    with open(tokenizer_path, 'r', encoding='utf-8') as f:
        tokenizer_json = json.load(f)

    # Add language to tokenizer
    tokenizer_json['model']['language'] = language

    with open(tokenizer_path, 'w', encoding='utf-8') as f:
        json.dump(tokenizer_json, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_path = "bpe_train_text.txt"
    tokenizer_path = "vietnamese_bpe_tokenizer.json"
    train_tokenizer(input_path, tokenizer_path, language='vi')