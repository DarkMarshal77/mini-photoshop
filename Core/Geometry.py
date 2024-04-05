from PIL import Image
import numpy as np


def rotate(image: np.ndarray, clockwise: bool):
    if clockwise:
        return image.swapaxes(0, 1)[:, ::-1, :]
    else:
        return image.swapaxes(0, 1)[::-1, :, :]


def flip(image: np.ndarray, vertical: bool):
    if vertical:
        return image[::-1, :, :]
    return image[:, ::-1, :]
