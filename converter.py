import tkinter as tk
from tkinter import ttk, messagebox

def convert():
    value = entry.get().strip()
    conversion = combo.get()

    try:
        if conversion == "Decimal → Binary":
            result = bin(int(value))[2:]

        elif conversion == "Decimal → Hex":
            result = hex(int(value))[2:].upper()

        elif conversion == "Binary → Decimal":
            result = str(int(value, 2))

        elif conversion == "Binary → Hex":
            result = hex(int(value, 2))[2:].upper()

        elif conversion == "Hex → Decimal":
            result = str(int(value, 16))

        elif conversion == "Hex → Binary":
            result = bin(int(value, 16))[2:]

        else:
            result = "Invalid conversion"

        output_label.config(text="Result: " + result)

    except ValueError:
        messagebox.showerror("Error", "Invalid input for selected conversion")

# Create window
root = tk.Tk()
root.title("Number Base Converter")
root.geometry("350x200")
root.resizable(False, False)

# Title
title = tk.Label(root, text="Number Converter", font=("Arial", 14))
title.pack(pady=10)

# Dropdown menu
options = [
    "Decimal → Binary",
    "Decimal → Hex",
    "Binary → Decimal",
    "Binary → Hex",
    "Hex → Decimal",
    "Hex → Binary"
]

combo = ttk.Combobox(root, values=options, state="readonly")
combo.set("Select Conversion")
combo.pack(pady=5)

# Entry box
entry = tk.Entry(root, width=25)
entry.pack(pady=5)

# Convert button
convert_btn = tk.Button(root, text="Convert", command=convert)
convert_btn.pack(pady=10)

# Output label
output_label = tk.Label(root, text="Result: ", font=("Arial", 12))
output_label.pack(pady=5)

# Run app
root.mainloop()