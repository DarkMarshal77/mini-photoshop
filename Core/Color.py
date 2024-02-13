from PIL import Image
from PIL import ImageEnhance


def convert_to_grayscale(image):
    return image.convert("L")


def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def adjust_color_balance(image, red_factor, green_factor, blue_factor):
    r, g, b = image.split()
    r = r.point(lambda p: p * red_factor)
    g = g.point(lambda p: p * green_factor)
    b = b.point(lambda p: p * blue_factor)
    return Image.merge("RGB", (r, g, b))
