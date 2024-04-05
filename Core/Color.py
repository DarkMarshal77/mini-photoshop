import numpy as np
import cv2


def convert_to_grayscale(image: np.ndarray):
    return np.dot(image[..., :3], [0.299, 0.587, 0.114])


def adjust_brightness(image: np.ndarray, factor: float):
    if len(image.shape) == 3:
        ycc = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2YCrCb)
        ycc[..., 0] = np.clip(ycc[..., 0] * factor, 0, 255).astype(np.uint8)
        return cv2.cvtColor(ycc, cv2.COLOR_YCrCb2RGB)
    else:
        return np.clip(image * factor, 0, 255).astype(np.uint8)


def adjust_contrast(image: np.ndarray, factor: float):
    if len(image.shape) == 3:
        ycc = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2YCrCb)
        ycc[..., 0] = np.clip(128 + ycc[..., 0] * factor - factor * 128, 0, 255).astype(np.uint8)
        return cv2.cvtColor(ycc, cv2.COLOR_YCrCb2RGB)
    else:
        return np.clip(128 + image * factor - factor * 128, 0, 255).astype(np.uint8)


def adjust_color_balance(image: np.ndarray, red_factor: float, green_factor: float, blue_factor: float):
    adjusted = image.copy()
    if len(adjusted.shape) == 3:
        adjusted[..., 0] = np.clip(adjusted[..., 0] * red_factor, 0, 255).astype(np.uint8)
        adjusted[..., 1] = np.clip(adjusted[..., 1] * green_factor, 0, 255).astype(np.uint8)
        adjusted[..., 2] = np.clip(adjusted[..., 2] * blue_factor, 0, 255).astype(np.uint8)
    return adjusted
