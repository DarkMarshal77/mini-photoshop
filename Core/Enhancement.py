import numpy as np
import cv2


def auto_level(image: np.ndarray):
    ycc = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)

    black = np.min(ycc[..., 0])
    white = np.max(ycc[..., 0])
    ycc[..., 0] = (ycc[..., 0] - black) * (255 / (white - black))

    auto_leveled = cv2.cvtColor(ycc, cv2.COLOR_YCrCb2RGB)
    return np.require(auto_leveled, np.uint8, 'C'), auto_leveled.shape[0], auto_leveled.shape[1]


def sharpen(image):
    pass


def histogram_equalization(image: np.ndarray):
    ycc = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)

    histogram, _ = np.histogram(ycc[..., 0], bins=256, range=(0, 256))
    cdf = histogram.cumsum()
    cdf_normalized = cdf * (255 / cdf[-1])
    ycc[..., 0] = np.uint8(cdf_normalized)[ycc[..., 0]]

    equalized = cv2.cvtColor(ycc, cv2.COLOR_YCrCb2RGB)
    return np.require(equalized, np.uint8, 'C'), equalized.shape[0], equalized.shape[1]
