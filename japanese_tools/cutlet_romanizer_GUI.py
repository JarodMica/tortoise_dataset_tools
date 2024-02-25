'''
Just a quick little GUI to see how cutlet romanizes Japanese input text
'''

import tkinter as tk
from tkinter import ttk
import cutlet

def convert_to_romaji():
    japanese_text = input_text.get("1.0", tk.END)
    katsu = cutlet.Cutlet()
    romaji_text = katsu.romaji(japanese_text)
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", romaji_text)

# Set up the main window
root = tk.Tk()
root.title("Japanese to Romaji Converter")

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

# Add a convert button
convert_button = ttk.Button(button_frame, text="Convert to Romaji", command=convert_to_romaji)
convert_button.pack(side=tk.RIGHT)

# Create a frame for the output area
output_frame = ttk.Frame(root, padding="10")
output_frame.pack(fill=tk.BOTH, expand=True)

# Add a label and text box for Romaji output
output_label = ttk.Label(output_frame, text="Romaji Text:")
output_label.pack(anchor=tk.W)
output_text = tk.Text(output_frame, height=10)
output_text.pack(fill=tk.BOTH, expand=True, pady="5")

root.mainloop()
