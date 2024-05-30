'''
Just a quick little GUI to see how cutlet romanizes Japanese input text
and how pykakasi converts it to hiragana.
'''

import tkinter as tk
from tkinter import ttk
import cutlet
import pykakasi

def convert_to_romaji():
    japanese_text = input_text.get("1.0", tk.END).strip()
    katsu = cutlet.Cutlet()
    romaji_text = katsu.romaji(japanese_text)
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", romaji_text)
    
def convert_to_hiragana():
    japanese_text = input_text.get("1.0", tk.END).strip()
    kakasi = pykakasi.kakasi()
    kakasi.setMode("J", "H")  # Japanese to Hiragana
    converter = kakasi.getConverter()
    hiragana_text = converter.do(japanese_text)
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", hiragana_text)

# Set up the main window
root = tk.Tk()
root.title("Japanese Text Converter")

# Create a frame for the input area
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill=tk.BOTH, expand=True)

# Add a label and text box for Japanese input
input_label = ttk.Label(input_frame, text="Japanese Text:")
input_label.pack(anchor=tk.W)
input_text = tk.Text(input_frame, height=10)
input_text.pack(fill=tk.BOTH, expand=True, pady="5")

# Create a frame for the buttons
button_frame = ttk.Frame(root, padding="10")
button_frame.pack(fill=tk.X, expand=True)

# Add convert buttons
convert_romaji_button = ttk.Button(button_frame, text="Convert to Romaji", command=convert_to_romaji)
convert_romaji_button.pack(side=tk.RIGHT, padx="10")

convert_hiragana_button = ttk.Button(button_frame, text="Convert to Hiragana", command=convert_to_hiragana)
convert_hiragana_button.pack(side=tk.RIGHT)

# Create a frame for the output area
output_frame = ttk.Frame(root, padding="10")
output_frame.pack(fill=tk.BOTH, expand=True)

# Add a label and text box for output
output_label = ttk.Label(output_frame, text="Output Text:")
output_label.pack(anchor=tk.W)
output_text = tk.Text(output_frame, height=10)
output_text.pack(fill=tk.BOTH, expand=True, pady="5")

root.mainloop()
