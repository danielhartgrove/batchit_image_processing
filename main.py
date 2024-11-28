from PIL import Image
import os
from heic2png import HEIC2PNG


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


if __name__ == '__main__':
    queue = []
    item = ""
    print("Add to Queue (:Q to end):")
    while item != ":Q":
        item = input()
        if item != ":Q":
            queue.insert(0, item)

    print("What would you like to do to the file(s)?")
    print("1. Convert webp to png (WEBP)")
    print("2. Convert heic to png (HEIC)")
    print("3. Rename (RENAME)")
    type = input()
    if type == "WEBP":
        print("Ok.")
        while len(queue) != 0:
            convert_webp_png(queue.pop(0))
    elif type == "HEIC":
        print("Ok.")
        while len(queue) != 0:
            convert_heic_png(queue.pop(0))
    elif type == "RENAME":
        print("Ok.")
        print("What to rename file(s)", "to?")
        rename_name = input()
        temp = rename_name
        count = 0
        while len(queue) != 0:
            path = queue.pop(0)
            if count != 0:
                rename_name = rename_name + "(" + str(count) + ")"
            rename(path, rename_name)
            rename_name = temp
    else:
        print("CHOICE DOES NOT EXIST")