import json

# Load the existing tokenizer
with open('tokenizer.json', 'r') as file:
    tokenizer = json.load(file)

# Define new special tokens
new_special_tokens = ["[angry]",
                      "[calm]",
                      "[disgust]",
                      "[fearful]",
                      "[happy]",
                      "[neutral]",
                      "[sad]",
                      "[surprised]"]

# Add special tokens to the added_tokens list and vocabulary
existing_max_id = max(token['id'] for token in tokenizer['added_tokens'])
vocab_size = len(tokenizer['model']['vocab'])

for idx, token in enumerate(new_special_tokens, start=existing_max_id + 1):
    # Ensure the ID is consistent
    new_id = vocab_size + idx - existing_max_id - 1

    # Add to added_tokens list
    tokenizer['added_tokens'].append({
        'id': new_id,
        'special': True,
        'content': token,
        'single_word': False,
        'lstrip': False,
        'rstrip': False,
        'normalized': False
    })

    # Add to vocab
    tokenizer['model']['vocab'][token] = new_id

# Save the updated tokenizer
with open('tokenizer_emotion.json', 'w') as file:
    json.dump(tokenizer, file, indent=2)
