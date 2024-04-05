from PIL import Image
from PIL import ImageEnhance

import numpy as np


def convert_to_grayscale(image: np.ndarray):
    weights = [0.299, 0.587, 0.114]  # RGB weights
    gray = np.dot(image[..., :3], weights).astype(np.uint8)
    return np.require(gray, np.uint8, 'C'), gray.shape[0], gray.shape[1]


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
