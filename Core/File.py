from PIL import Image


def open_image(file_path):
    try:
        image = Image.open(file_path)
        return image
    except FileNotFoundError:
        print("File not found. Please provide a valid image file path.")
        return None


def save_as(image, path, format):
    pass
