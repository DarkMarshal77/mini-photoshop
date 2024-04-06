import numpy as np
import cv2


def auto_level(image: np.ndarray):
    if len(image.shape) == 3:
        ycc = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2YCrCb)
        black = np.min(ycc[..., 0])
        white = np.max(ycc[..., 0])
        ycc[..., 0] = (ycc[..., 0] - black) * (255 / (white - black))
        return cv2.cvtColor(ycc, cv2.COLOR_YCrCb2RGB)
    else:
        black = np.min(image)
        white = np.max(image)
        return (image - black) * (255 / (white - black))


def histogram_equalization(image: np.ndarray):
    if len(image.shape) == 3:
        ycc = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2YCrCb)
        histogram, _ = np.histogram(ycc[..., 0], bins=256, range=(0, 256))
        cdf = histogram.cumsum()
        ycc[..., 0] = np.round(255 * (cdf[ycc[..., 0]] - cdf[0]) / (cdf[-1] - cdf[0]))
        return cv2.cvtColor(ycc, cv2.COLOR_YCrCb2RGB)
    else:
        int_image = image.astype(np.uint8)
        histogram, _ = np.histogram(int_image, bins=256, range=(0, 256))
        cdf = histogram.cumsum()
        return np.round(255 * (cdf[int_image] - cdf[0]) / (cdf[-1] - cdf[0]))
