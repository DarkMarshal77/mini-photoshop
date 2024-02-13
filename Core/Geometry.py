from PIL import Image


def resize_image(image, new_width, new_height):
    return image.resize((new_width, new_height))


def crop_image(image, left, top, right, bottom):
    return image.crop((left, top, right, bottom))


def rotate(image):
    return image.rotate(90)


def flip(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)
