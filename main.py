from PIL import Image
import os
from heic2png import HEIC2PNG
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_webp_png(path: str):
    webp_path = (path.replace("\"", "").replace("\'", ""))
    # remove any quotes from the input

    if not os.path.exists(webp_path):
        print("File " + webp_path + " does not exist")
        exit(1)

    webp_image = Image.open(webp_path)
    webp_image = webp_image.convert('RGB')

    webp_path = webp_path.lower()
    new_path = webp_path.replace(".webp", ".png")

    try:
        webp_image.save(new_path)  # The converted image will be saved as `test.png'
        print(new_path)
    except FileExistsError:
        print("File " + new_path + " already exists")

def convert_heic_png(path: str):
    heic_path = (path.replace("\"", "").replace("\'", ""))

    if not os.path.exists(heic_path):
        print("File " + heic_path + " does not exist")
        exit(1)

    heic_image = HEIC2PNG(heic_path, quality=100)  # Specify the quality of the converted image
    new_path = heic_path.replace(".HEIC", ".png")

    try:
        heic_image.save(new_path)  # The converted image will be saved as `test.png'
        print(new_path)
    except FileExistsError:
        print("File " + new_path + " already exists")

def rename(file_path: str, newname: str):
    file_path = (file_path.replace("\"", "").replace("\'", ""))
    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found.")
        return

    filename, extension = os.path.splitext(file_path)
    new_file_path = os.path.join(os.path.dirname(file_path), f"{newname}{extension}")

    try:
        os.rename(file_path, new_file_path)
        print(f"File renamed successfully: {file_path} -> {new_file_path}")
    except OSError as error:
        print(f"Error renaming file: {error}")

def add_file_path():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_list.insert(tk.END, file_path)

def process_file(index):
    file_path = file_list.get(index)
    print(f"Processing file: {file_path}")

def remove_file(index):
    file_list.delete(index)

# Create the main window
window = tk.Tk()
window.title("BatchIt!")

# Create a frame for the listbox
listbox_frame = tk.LabelFrame(window, text="Files")
listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the listbox
file_list = tk.Listbox(listbox_frame, height=10, width=30)
file_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a frame for buttons
button_frame = tk.LabelFrame(window, text="Functions")
button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Create buttons
add_button = tk.Button(button_frame, text="Add File", command=add_file_path)
add_button.pack(pady=5, padx=5)

convert_button = tk.Button(button_frame, text="to PNG", command=lambda: convert_heic_png(file_list.curselection()[0]))
convert_button.pack(pady=5, padx=5)

rename_button = tk.Button(button_frame, text="Rename", command=lambda: rename_popup(file_list.curselection()[0]))
rename_button.pack(pady=5, padx=5)

threshold_button = tk.Button(button_frame, text="Threshold", command=lambda: threshold_popup(file_list.curselection()[0]))
threshold_button.pack(pady=5, padx=5)

remove_button = tk.Button(button_frame, text="Remove", command=lambda: remove_file(file_list.curselection()[0]))
remove_button.pack(pady=5, padx=5)

window.mainloop()