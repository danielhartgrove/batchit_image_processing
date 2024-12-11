from PIL import Image
import os
from errors import *
from heic2png import HEIC2PNG
import tkinter as tk
from tkinter import filedialog, messagebox

# Conversion Functions

# FUCKING DYNAMIC TYPING >:(
def convert_webp_png(path: str):
    """
    Function to convert webp image to png
    :param path: the path of the webp image to convert
    :return: the filepath of the png image
    """
    webp_path = (path.replace("\"", "").replace("\'", ""))
    # remove any quotes from the input

    if not webp_path.endswith(".webp"):
        raise NotHEICError

    if not os.path.exists(webp_path):
        print("File " + webp_path + " does not exist")
        raise FileNotFoundError

    webp_image = Image.open(webp_path)
    webp_image = webp_image.convert('RGB')

    webp_path = webp_path.lower()
    new_path = webp_path.replace(".webp", ".png")

    try:
        webp_image.save(new_path)  # The converted image will be saved as `test.png'
        return new_path
    except FileExistsError:
        print("File " + new_path + " already exists")
def convert_webp_png_caller(selection: tuple):
    """
    Function to convert webp image to png
    :param path: the path of the webp image to convert
    :return: the filepath of the png image
    """

    for path in selection:
       convert_webp_png(path)

def convert_heic_png(path: str):
    """
     Function to convert heic image to png
    :param path: the path of the heic to be converted to png
    :return: path of the new file
    """
    heic_path = (path.replace("\"", "").replace("\'", ""))

    if not heic_path.endswith(".heic"):
        raise NotHEICError

    if not os.path.exists(heic_path):
        print("File " + heic_path + " does not exist")
        raise FileNotFoundError

    heic_image = HEIC2PNG(heic_path, quality=100)  # Specify the quality of the converted image
    new_path = heic_path.replace(".heic", ".png")

    try:
        heic_image.save(new_path)  # The converted image will be saved as `test.png'
        return new_path
    except FileExistsError:
        print("File " + new_path + " already exists")
def convert_heic_png_caller(selection: tuple):
    """
     Function to convert heic image to png
    :param path: the path of the heic to be converted to png
    :return: path of the new file
    """
    for path in selection:
        convert_heic_png(path)

def rename(path: str, newname: str):
    """
    Function to rename a file to a provided name
    :param selection: the paths of the files to be renamed
    :param newname: the new name of the file
    :return: bool True if successful, False if unsuccessful
    """
    file_path = (path.replace("\"", "").replace("\'", ""))
    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found.")
        raise FileNotFoundError

    filename, extension = os.path.splitext(file_path)
    new_file_path = os.path.join(os.path.dirname(file_path), f"{newname}{extension}")

    try:
        os.rename(file_path, new_file_path)
        print(f"File renamed successfully: {file_path} -> {new_file_path}")
    except OSError as error:
        print(f"Error renaming file: {error}")
def rename_caller(selection: tuple, newname: str):
    """
    Function to rename a file to a provided name
    :param selection: the paths of the files to be renamed
    :param newname: the new name of the file
    :return: bool True if successful, False if unsuccessful
    """

    for file_path in selection:
        file_path = (file_path.replace("\"", "").replace("\'", ""))
        if not os.path.exists(file_path):
            print(f"File '{file_path}' not found.")
            raise FileNotFoundError

        filename, extension = os.path.splitext(file_path)
        new_file_path = os.path.join(os.path.dirname(file_path), f"{newname}{extension}")

        try:
            os.rename(file_path, new_file_path)
            print(f"File renamed successfully: {file_path} -> {new_file_path}")
        except OSError as error:
            print(f"Error renaming file: {error}")

def threshold(path: str, value: int):
    try:
        img = Image.open(path).convert('L')  # Convert to grayscale
        threshold_img = img.point(lambda p: p > value and 255)
        threshold_img.save(path)
    except FileNotFoundError:
        raise FileNotFoundError
def threshold_caller(selection: tuple, value: int):
    for path in selection:
        threshold(path, value)

#List Functions
def add_file_path():
    """
    Function to add a file to the file_list
    """
    file_path = filedialog.askopenfilename()
    if file_path:
        file_list.insert(tk.END, file_path)

def remove_file(index):
    """
    Function to remove a file from the file_list
    :param index: the index of the file to be removed
    """
    file_list.delete(index)

# TKinter Functions
def threshold_popup(selection):
    popup = tk.Toplevel()
    popup.title("Threshold File(s)")

    # Create a slider
    slider = tk.Scale(popup, from_=0, to=255, orient=tk.HORIZONTAL)
    slider.pack(pady=10)

    # Create a button
    button = tk.Button(popup, text="Threshold", command=lambda: threshold(selection, slider.get()))
    button.pack(pady=10)

def rename_popup(selection):
    popup = tk.Toplevel()
    popup.title("Rename File(s)")

    # Create a label and text entry box
    label = tk.Label(popup, text="Enter the new file name:")
    label.pack()

    text_entry = tk.Entry(popup)
    text_entry.pack()

    # Create a button to trigger the text retrieval
    button = tk.Button(popup, text="Submit", command=rename(selection, text_entry.get()))
    button.pack()


if __name__ == "__main__":
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

    convert_button = tk.Button(button_frame, text="to PNG", command=lambda: convert(file_list.curselection()[0]))
    convert_button.pack(pady=5, padx=5)

    rename_button = tk.Button(button_frame, text="Rename", command=lambda: rename_popup(file_list.curselection()[0]))
    rename_button.pack(pady=5, padx=5)

    threshold_button = tk.Button(button_frame, text="Threshold", command=lambda: threshold_popup(file_list.curselection()))
    threshold_button.pack(pady=5, padx=5)

    remove_button = tk.Button(button_frame, text="Remove", command=lambda: remove_file(file_list.curselection()[0]))
    remove_button.pack(pady=5, padx=5)

    window.mainloop()